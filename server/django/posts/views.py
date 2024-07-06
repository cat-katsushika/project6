# posts/views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# posts/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import VideoForm
from .models import Video



def video_list(request):
    videos = Video.objects.all().order_by("-uploaded_at")
    return render(request, "posts/video_list.html", {"videos": videos})


def video_map_api(request):
    videos = Video.objects.all()
    video_data = []
    for video in videos:
        if video.latitude and video.longitude and video.thumbnail_file and video.video_file:
            avatar_url = video.user.avatar.url
            video_data.append(
                {
                    "id": video.id,
                    "latitude": video.latitude,
                    "longitude": video.longitude,
                    "thumbnail_url": video.thumbnail_file.url,
                    "avatar_url": avatar_url,
                    "username": video.user.username,
                    "uploaded_at": video.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            )
    return JsonResponse(video_data, safe=False)


def video_map(request):
    return render(request, "posts/video_map.html")


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, "posts/video_detail.html", {"video": video})


class UploadVideoView(LoginRequiredMixin, TemplateView):
    template_name = "posts/upload_video.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["message"] = "Hello, World!"
        context["form"] = VideoForm()
        return context

    def post(self, request, *args, **kwargs):
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")
        video_file = request.FILES.get("video_file")
        thumbnail_file = request.FILES.get("thumbnail_file")

        context = self.get_context_data(**kwargs)

        if not (latitude and longitude and video_file and thumbnail_file):
            context["error"] = "位置情報、動画ファイル、サムネイルファイルの全てが必要です。"
            return self.render_to_response(context)

        video_form = VideoForm(request.POST, request.FILES)
        if video_form.is_valid():
            video = video_form.save(commit=False)
            video.user = request.user
            video.latitude = float(latitude)
            video.longitude = float(longitude)
            video.video_file = video_file
            video.thumbnail_file = thumbnail_file
            video.save()
            return redirect("posts:video_list")
        else:
            # debug
            context["form_errors"] = video_form.errors
            context["form"] = video_form

        return self.render_to_response(context)
    

