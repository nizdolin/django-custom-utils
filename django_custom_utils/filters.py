from django.contrib.admin import SimpleListFilter
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import \
    RelatedOnlyDropdownFilter as BaseRelatedOnlyDropdownFilter
from django_filters import rest_framework as filters


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ChoiceInFilter(filters.BaseInFilter, filters.ChoiceFilter):
    pass


class RelatedOnlyDropdownFilter(BaseRelatedOnlyDropdownFilter):
    def field_choices(self, field, request, model_admin):
        field_choices = super().field_choices(field, request, model_admin)
        return sorted(field_choices, key=lambda i: i[1])


class BooleanDefaultNoFilter(SimpleListFilter):
    def lookups(self, request, model_admin) -> tuple:
        return ("all", _("All")), (1, _("Yes")), (None, _("No"))

    def choices(self, changelist) -> dict:
        for lookup, title in self.lookup_choices:  # noqa: WPS526
            yield {
                "selected": self.value()
                == (str(lookup) if lookup else lookup),  # noqa: WPS509
                "query_string": changelist.get_query_string(
                    {self.parameter_name: lookup}, []
                ),
                "display": title,
            }

    def queryset(self, request, queryset) -> QuerySet:
        if self.value():
            if self.value() == "all":
                return queryset
            else:
                return queryset.filter(**{self.parameter_name: self.value()})

        elif self.value() is None:
            return queryset.filter(**{self.parameter_name: False})
