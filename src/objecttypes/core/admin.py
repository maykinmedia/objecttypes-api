from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

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
