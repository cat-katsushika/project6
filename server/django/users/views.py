from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from posts.models import Video

User = get_user_model()


class HomePageView(TemplateView):
    template_name = "users/home.html"


class ProfilePageView(TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = User.objects.get(pk=self.kwargs["user_id"])
        videos = Video.objects.filter(user=context["profile"]).order_by("-uploaded_at")
        context["videos"] = videos
        context["video_count"] = len(videos)

        return context
