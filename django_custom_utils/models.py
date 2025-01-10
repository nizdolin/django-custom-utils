import re

import uuid6
from django.contrib.contenttypes.models import ContentType
from django.db import OperationalError, ProgrammingError, models
from django.urls import reverse
from django.utils.functional import classproperty
from django.utils.html import conditional_escape, format_html
from django.utils.translation import gettext_lazy as _

from django_custom_utils import utils
from django_custom_utils.managers import ActiveManager


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True

    @classproperty
    def app_label(cls) -> str:  # noqa
        return cls._meta.app_label  # noqa

    @classproperty
    def model_name(cls) -> str:  # noqa
        return cls._meta.model_name  # noqa

    @classproperty
    def verbose_name(cls) -> str:  # noqa
        return cls._meta.verbose_name  # noqa

    @classproperty
    def verbose_name_plural(cls) -> str:  # noqa
        return re.sub("^\d+\. ", "", cls._meta.verbose_name_plural)  # noqa

    @classmethod
    def get_index_url(cls, **kwargs) -> str:
        path = reverse(f"admin:{cls.app_label}_{cls.model_name}_changelist")
        return utils.site_url(path, **kwargs)

    @utils.cached_classproperty
    def self_content_type_id(cls):  # noqa
        try:
            content_type_id = ContentType.objects.get_for_model(cls).id
        except (ProgrammingError, OperationalError):
            content_type_id = None

        return content_type_id

    @utils.cached_classproperty
    def content_type_id(cls):  # noqa
        return cls.self_content_type_id

    def get_url(self, **kwargs) -> str:
        path = reverse(
            f"admin:{self.app_label}_{self.model_name}_change", args=[self.pk]
        )
        return utils.site_url(path, **kwargs)

    def get_link(self, title="", attr=None) -> str:
        if not self.pk:
            return "-"
        if not title and attr and hasattr(self, attr):
            title = getattr(self, attr)
        title = title or str(self)
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            self.get_url(),
            conditional_escape(title),
        )

    @classmethod
    def get_field(cls, field_name):
        return cls._meta.get_field(field_name)  # noqa


class ActiveModel(BaseModel):
    active = models.BooleanField(default=True, verbose_name=_("Is active?"))

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True


class UUID8Model(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid6.uuid8, editable=False)

    class Meta:
        abstract = True


class CreatedAtModel(BaseModel):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True, blank=True)

    class Meta:
        abstract = True


class UpdatedAtModel(BaseModel):
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True, blank=True)

    class Meta:
        abstract = True


class TimeStampedModel(CreatedAtModel, UpdatedAtModel):
    class Meta:
        abstract = True


def merge_model_objects(
    primary_object: BaseModel, alias_objects: BaseModel | list, keep_old: bool = False
):
    """
    Use this function to merge model objects (i.e. Users, Organizations, Polls,
    etc.) and migrate all the related fields from the alias objects to the
    primary object.

    Usage:
    from django.contrib.auth.models import User
    primary_user = User.objects.get(email='good_email@example.com')
    duplicate_user = User.objects.get(email='good_email+duplicate@example.com')
    merge_model_objects(primary_user, duplicate_user)
    """

    if not isinstance(alias_objects, list):
        alias_objects = [alias_objects]

    # check that all aliases are the same class as primary one and that
    # they are subclass of model
    primary_class = primary_object.__class__

    if not issubclass(primary_class, BaseModel):
        raise TypeError("Only BaseModel subclasses can be merged")

    blank_local_fields = {
        field.attname
        for field in primary_object._meta.local_fields  # noqa: WPS437
        if getattr(primary_object, field.attname) in [None, ""]
    }

    # Loop through all alias objects and migrate their data to the primary object.
    for alias_object in alias_objects:
        if not isinstance(alias_object, primary_class):
            raise TypeError("Only models of same class can be merged")

        # Migrate all foreign key references from alias object to primary object.
        for related_object in alias_object._meta.related_objects:  # noqa: WPS437
            # The variable name on the alias_object model.
            alias_varname = related_object.get_accessor_name()
            # The variable name on the related model.
            obj_varname = related_object.field.name
            try:
                alias_related_objects = getattr(alias_object, alias_varname)
            except Exception:
                if related_object.one_to_one:
                    continue
                else:
                    raise

            if isinstance(alias_related_objects, BaseModel):
                continue

            for obj in alias_related_objects.all():
                setattr(obj, obj_varname, primary_object)
                obj.save()

        # Try to fill all missing values in primary object by values of duplicates
        filled_up = set()
        for field_name in blank_local_fields:
            val = getattr(alias_object, field_name)
            if val not in [None, ""]:
                setattr(primary_object, field_name, val)
                filled_up.add(field_name)
        blank_local_fields -= filled_up

        if not keep_old:
            alias_object.delete()
    primary_object.save()
    return primary_object
