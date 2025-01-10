from django import forms
from django.contrib.postgres.fields import ArrayField
from django.db import models

from django_custom_utils.models import BaseModel


class BaseForeignMixin:
    def __init__(
        self,
        to,
        on_delete=models.CASCADE,
        related_name=None,
        related_query_name=None,
        limit_choices_to=None,
        parent_link=False,
        to_field=None,
        db_constraint=True,
        **kwargs
    ) -> None:
        if (
            "verbose_name" not in kwargs
            and not isinstance(to, str)
            and issubclass(to, BaseModel)
        ):
            kwargs["verbose_name"] = to.verbose_name

        super().__init__(
            to,
            on_delete=on_delete,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            parent_link=parent_link,
            to_field=to_field,
            db_constraint=db_constraint,
            **kwargs
        )


class ForeignKey(BaseForeignMixin, models.ForeignKey): ...


class OneToOneField(BaseForeignMixin, models.OneToOneField): ...


class ManyToManyField(models.ManyToManyField):
    def __init__(
        self,
        to,
        related_name=None,
        related_query_name=None,
        limit_choices_to=None,
        symmetrical=None,
        through=None,
        through_fields=None,
        db_constraint=True,
        db_table=None,
        swappable=True,
        **kwargs
    ) -> None:
        if (
            "verbose_name" not in kwargs
            and not isinstance(to, str)
            and issubclass(to, BaseModel)
        ):
            kwargs["verbose_name"] = to.verbose_name_plural

        super().__init__(
            to,
            related_name=related_name,
            related_query_name=related_query_name,
            limit_choices_to=limit_choices_to,
            symmetrical=symmetrical,
            through=through,
            through_fields=through_fields,
            db_constraint=db_constraint,
            db_table=db_table,
            swappable=swappable,
            **kwargs
        )


class ChoiceArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.TypedMultipleChoiceField,
            "choices": self.base_field.choices,
            "coerce": self.base_field.to_python,
            "widget": forms.CheckboxSelectMultiple,
        } | kwargs
        return super().formfield(**defaults)
