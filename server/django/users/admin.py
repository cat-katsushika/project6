from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "id", "avatar")
    search_fields = ("username",)
    ordering = ("username",)
    list_filter = ("username",)
