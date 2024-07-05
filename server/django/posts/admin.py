from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("user", "uploaded_at", "video_file", "thumbnail_file", "latitude", "longitude")
    list_filter = ("user", "uploaded_at")
    search_fields = ("user__username",)
    ordering = ("-uploaded_at",)
