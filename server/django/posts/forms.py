# posts/forms.py
from django import forms

from .models import Video


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["video_file", "thumbnail_file", "latitude", "longitude"]


class VideoMemoUpdateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["memo"]
