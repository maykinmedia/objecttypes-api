import json

from django.contrib import admin, messages
from django.contrib.postgres.fields import JSONField
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from jsonsuit.widgets import READONLY_WIDGET_MEDIA_CSS, READONLY_WIDGET_MEDIA_JS
from sharing_configs.admin import SharingConfigsExportMixin, SharingConfigsImportMixin

from .constants import ObjectVersionStatus
from .forms import ObjectVersionForm, UrlImportForm
from .models import ObjectType, ObjectVersion
from .utils import check_json_schema
from .widgets import JSONSuit


def can_change(obj) -> bool:
    if not obj:
        return True

    if not obj.last_version:
        return True

    if obj.last_version.status == ObjectVersionStatus.draft:
        return True

    return False


class ObjectVersionInline(admin.StackedInline):
    verbose_name_plural = _("last version")
    model = ObjectVersion
    form = ObjectVersionForm
    extra = 0
    max_num = 1
    min_num = 1
    readonly_fields = ("version", "status", "published_at")
    formfield_overrides = {JSONField: {"widget": JSONSuit}}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        parent_id = request.resolver_match.kwargs.get("object_id")
        if not parent_id:
            return queryset

        last_version = (
            queryset.filter(object_type_id=parent_id).order_by("-version").first()
        )
        if not last_version:
            return queryset.none()
        return queryset.filter(id=last_version.id)

    def has_delete_permission(self, request, obj=None):
        return False

    # work around to prettify readonly JSON field
    def get_exclude(self, request, obj=None):
        if not can_change(obj):
            return ("json_schema",)
        return super().get_exclude(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not can_change(obj):
            local_fields = [field.name for field in self.opts.local_fields]
            # work around to prettify readonly JSON field
            local_fields.remove("json_schema")
            local_fields.append("json_schema_readonly")
            return local_fields

        return super().get_readonly_fields(request, obj)

    def json_schema_readonly(self, obj):
        return format_html(
            '<div class="suit"><pre><code class="language-json">{}</code></pre></div>',
            json.dumps(obj.json_schema, indent=2),
        )

    json_schema_readonly.short_description = "JSON schema"

    class Media:
        js = READONLY_WIDGET_MEDIA_JS
        css = READONLY_WIDGET_MEDIA_CSS


@admin.register(ObjectType)
class ObjectTypeAdmin(
    SharingConfigsImportMixin, SharingConfigsExportMixin, admin.ModelAdmin
):
    list_display = ("name", "name_plural", "allow_geometry")
    search_fields = ("uuid",)
    inlines = [ObjectVersionInline]

    change_list_template = "admin/core/objecttype/object_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "import-from-url/",
                self.admin_site.admin_view(self.import_from_url_view),
                name="import_from_url",
            ),
        ]
        return my_urls + urls

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)

        if obj:
            readonly_fields = ("uuid",) + readonly_fields

        return readonly_fields

    def publish(self, request, obj):
        last_version = obj.last_version
        last_version.status = ObjectVersionStatus.published
        last_version.save()

        msg = format_html(
            _("The object type {version} has been published successfully!"),
            version=obj.last_version,
        )
        self.message_user(request, msg, level=messages.SUCCESS)

        return HttpResponseRedirect(request.path)

    def add_new_version(self, request, obj):
        new_version = obj.last_version
        new_version.pk = None
        new_version.version = new_version.version + 1
        new_version.status = ObjectVersionStatus.draft
        new_version.save()

        msg = format_html(
            _("The new version {version} has been created successfully!"),
            version=new_version,
        )
        self.message_user(request, msg, level=messages.SUCCESS)

        return HttpResponseRedirect(request.path)

    def response_change(self, request, obj):
        if "_publish" in request.POST:
            return self.publish(request, obj)

        if "_newversion" in request.POST:
            return self.add_new_version(request, obj)

        return super().response_change(request, obj)

    def import_from_url_view(self, request):
        if request.method == "POST":
            form = UrlImportForm(request.POST)
            if form.is_valid():
                form_json = form.cleaned_data.get("json")

                ObjectType.objects.create_from_schema(
                    json_schema=form_json,
                    name_plural=form.data.get("name_plural", "").title(),
                )
                return redirect(reverse("admin:core_objecttype_changelist"))
        else:
            form = UrlImportForm()

        return render(
            request, "admin/core/objecttype/object_import_form.html", {"form": form}
        )

    def get_sharing_configs_import_data(self, content: bytes) -> ObjectType:
        json_schema = json.loads(content.decode())
        check_json_schema(json_schema)

        return ObjectType.objects.create_from_schema(json_schema)

    def get_sharing_configs_export_data(self, obj: ObjectType) -> bytes:
        json_schema_str = json.dumps(obj.last_version.json_schema)
        return json_schema_str.encode()
