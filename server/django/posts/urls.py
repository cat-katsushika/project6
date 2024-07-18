# posts/urls.py
from django.urls import path

from . import views

app_name = "posts"

urlpatterns = [
    path("upload/", views.UploadVideoView.as_view(), name="upload_video"),
    path("video_list", views.VideoListView.as_view(), name="video_list"),
    path("map/", views.VideoMapView.as_view(), name="video_map"),  # 地図表示用のテンプレートビュー
    path("map/data/", views.video_map_api, name="video_map_api"),  # 地図データ用のJSONビュー
    path("video/<uuid:video_id>/", views.video_detail, name="video_detail"),  # 動画詳細ページ
    path("video/<uuid:pk>/delete/", views.DeleteVideoView.as_view(), name="delete_video"),  # 動画削除ビュー
    path("video/<uuid:video_id>/regenerate_thumbnail/", views.regenerate_thumbnail, name="regenerate_thumbnail"),
    path("update-video-memo/<uuid:video_id>/", views.update_video_memo, name="update_video_memo"),
]
