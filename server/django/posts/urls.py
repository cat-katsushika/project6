# posts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_video, name='upload_video'),
    path('', views.video_list, name='video_list'),
    path('map/', views.video_map_page, name='video_map_page'),  # 地図表示用のテンプレートビュー
    path('map/data/', views.video_map, name='video_map_data'),  # 地図データ用のJSONビュー
    path('video/<int:video_id>/', views.video_detail, name='video_detail'),  # 動画詳細ページ
]
