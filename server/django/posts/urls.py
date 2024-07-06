# posts/urls.py
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("upload/", views.UploadVideoView.as_view(), name="upload_video"),
    path("video_list", views.video_list, name="video_list"),
    path("map/", views.video_map, name="video_map"),  # 地図表示用のテンプレートビュー
    path("map/data/", views.video_map_api, name="video_map_api"),  # 地図データ用のJSONビュー
    path("video/<uuid:video_id>/", views.video_detail, name="video_detail"),  # 動画詳細ページ
]
