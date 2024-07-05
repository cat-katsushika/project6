from django.urls import path

from .views import HomePageView, ProfilePageView

app_name = "users"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("users/profile/<uuid:user_id>", ProfilePageView.as_view(), name="profile"),
]
