from django.contrib import admin

from solo.admin import SingletonModelAdmin

from .models import GithubConfig


@admin.register(GithubConfig)
class GithubConfigAdmin(SingletonModelAdmin):
    pass
