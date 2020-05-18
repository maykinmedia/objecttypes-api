from django.contrib import admin

from .models import ObjectType, ObjectVersion


class ObjectVersionInline(admin.TabularInline):
    model = ObjectVersion
    extra = 1


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "name_plural")
    search_fields = ("uuid",)
    inlines = [ObjectVersionInline]
