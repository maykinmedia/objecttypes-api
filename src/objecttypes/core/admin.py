from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
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
        parent_id = request.resolver_match.kwargs.get("object_id")
        if not parent_id:
            return queryset

        last_version = (
            queryset.filter(object_type_id=parent_id).order_by("-version").first()
        )
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

    def response_change(self, request, obj):
        if "_publish" not in request.POST:
            return super().response_change(request, obj)

        last_version = obj.last_version
        last_version.status = ObjectVersionStatus.published
        last_version.save()

        msg = format_html(
            _("The object type {version} has been published successfully!"),
            version=obj.last_version,
        )
        self.message_user(request, msg, level=messages.SUCCESS)

        return HttpResponseRedirect(request.path)
