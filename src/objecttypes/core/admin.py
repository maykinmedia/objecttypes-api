from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .constants import ObjectVersionStatus
from .models import ObjectType, ObjectVersion


class ObjectVersionInline(admin.StackedInline):
    verbose_name_plural = _("last version")
    model = ObjectVersion
    extra = 0
    max_num = 1
    min_num = 1

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        last_version = queryset.order_by("-version").first()
        return queryset.filter(id=last_version.id)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "name_plural")
    search_fields = ("uuid",)
    inlines = [ObjectVersionInline]

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return super().get_readonly_fields(request, obj)

        # make all meta fields read_only when changing the existing object type
        field_names = [field.name for field in self.opts.local_fields]
        return field_names

    def has_change_permission(self, request, obj=None):
        if not obj or obj.last_version.status == ObjectVersionStatus.draft:
            return super().has_change_permission(request, obj)

        return False
