import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class PathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = "{}.{}".format(instance.id, ext)
        return os.path.join(self.sub_path, filename)


# 動画用のパスを指定します
video_upload_path = PathAndRename("videos/")
thumbnail_upload_path = PathAndRename("thumbnails/")


class Video(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video_file = models.FileField(upload_to=video_upload_path)
    thumbnail_file = models.ImageField(upload_to=thumbnail_upload_path)
    memo = models.TextField(max_length=100, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.uploaded_at}"
