import re

from django.contrib.contenttypes.models import ContentType
from django.db import models, ProgrammingError, OperationalError
from django.urls import reverse
from django.utils.functional import classproperty
from django.utils.html import conditional_escape, format_html

from django_custom_utils.managers import ActiveManager
from django_custom_utils import utils


__all__ = [
    'BaseModel',
    'CreatedAtModel',
    'DateTimeModel',
    'ActiveModel',
]


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True

    @classproperty
    def app_label(cls):  # noqa
        return cls._meta.app_label  # noqa

    @classproperty
    def model_name(cls):  # noqa
        return cls._meta.model_name  # noqa

    @classproperty
    def verbose_name(cls):  # noqa
        return cls._meta.verbose_name  # noqa

    @classproperty
    def verbose_name_plural(cls):  # noqa
        return re.sub('^\d+\. ', '', cls._meta.verbose_name_plural)  # noqa

    @classmethod
    def get_index_url(cls, **kwargs):
        path = reverse(f'admin:{cls.app_label}_{cls.model_name}_changelist')
        return utils.site_url(path, **kwargs)

    @utils.cached_classproperty
    def content_type_id(cls):  # noqa
        try:
            return ContentType.objects.get_for_model(cls).id
        except (ProgrammingError, OperationalError):
            return

    def get_admin_url(self, **kwargs):
        path = reverse(f'admin:{self.app_label}_{self.model_name}_change', args=[self.pk])
        return utils.site_url(path, **kwargs)

    def get_admin_link(self, title='', attr=None):
        if not self.pk:
            return '-'
        if not title and attr and hasattr(self, attr):
            title = getattr(self, attr)
        title = title or str(self)
        return format_html('<a href="{}" target="_blank">{}</a>', self.get_admin_url(), conditional_escape(title))


class CreatedAtModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Создано')

    class Meta:
        abstract = True


class DateTimeModel(CreatedAtModel):
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        abstract = True


class ActiveModel(BaseModel):
    is_active = models.BooleanField(default=True, verbose_name='Активно?')

    objects = models.Manager()
    active_objects = ActiveManager()

    class Meta:
        abstract = True
