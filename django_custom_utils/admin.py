from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin


__all__ = [
    'ModelAdmin',
    'BaseInline',
    'StackedInline',
    'TabularInline',
]


class ModelAdmin(admin.ModelAdmin):
    can_add = True
    can_change = True
    can_delete = True
    readonly = False

    def has_add_permission(self, request):
        if self.readonly or not self.can_add:
            return False
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if self.readonly or not self.can_change:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if self.readonly or not self.can_delete:
            return False
        return super().has_delete_permission(request, obj)


class BaseInline(InlineModelAdmin):
    readonly = False
    extra = 0

    def __init__(self, *args, **kwargs):
        if self.readonly:
            self.extra = 0
            self.readonly_fields = self.fields
        super().__init__(*args, **kwargs)

    def has_add_permission(self, request, obj):
        if self.readonly:
            return False
        return super().has_add_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if self.readonly:
            return False
        return super().has_delete_permission(request, obj)

    def get_extra(self, request, obj=None, **kwargs):
        if self.readonly:
            return 0
        return super().get_extra(request, obj, **kwargs)


class StackedInline(BaseInline):
    template = 'admin/edit_inline/stacked.html'


class TabularInline(BaseInline):
    template = 'admin/edit_inline/tabular.html'
