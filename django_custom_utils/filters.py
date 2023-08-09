from django_admin_listfilter_dropdown.filters import RelatedOnlyDropdownFilter as BaseRelatedOnlyDropdownFilter
from django_filters import rest_framework as filters


__all__ = [
    'NumberInFilter',
    'CharInFilter',
    'ChoiceInFilter',
    'RelatedOnlyDropdownFilter',
]


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
