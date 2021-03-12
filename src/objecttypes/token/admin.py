from django.contrib import admin

from .models import TokenAuth


@admin.register(TokenAuth)
class TokenAuthAdmin(admin.ModelAdmin):
    readonly_fields = ("token",)
    list_display = (
        "token",
        "contact_person",
        "organization",
        "administration",
        "application",
    )
