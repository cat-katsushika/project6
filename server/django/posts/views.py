# posts/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse

# posts/views.py
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView

from .forms import VideoForm, VideoMemoUpdateForm
from .models import Video
from .utils import generate_thumbnail


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


# 下部のHomeボタンで飛ぶ先のビュー
class PostListView(TemplateView):
    template_name = "posts/post_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Video.objects.all().order_by("-uploaded_at")
        return context


class VideoMapView(TemplateView):
    template_name = "posts/map.html"


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
            return redirect("users:profile", user_id=request.user.id)
        else:
            # debug
            context["form_errors"] = video_form.errors
            context["form"] = video_form

        return self.render_to_response(context)


class DeleteVideoView(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = "posts/video_confirm_delete.html"

    def get_success_url(self):
        return reverse("users:profile", kwargs={"user_id": self.request.user.id})

    def get_object(self, queryset=None):
        video = super().get_object()
        if video.user != self.request.user:
            raise PermissionDenied
        return video


@login_required
def regenerate_thumbnail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # if video.user != request.user:
    #     return HttpResponse('あなたの投稿ではありません', status=401)

    try:
        thumbnail_content = generate_thumbnail(video.video_file.path)
        video.thumbnail_file.save(thumbnail_content.name, thumbnail_content, save=True)
        return redirect("posts:video_detail", video_id=video.id)
    except Exception:
        return HttpResponse("サムネイルの再生成に失敗しました", status=500)


# videoのmemoを更新するAPI
@login_required
def update_video_memo(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if video.user != request.user:
        return JsonResponse({"status": "error", "message": "You are not authorized to update this memo."}, status=403)

    if request.method == "POST":
        form = VideoMemoUpdateForm(request.POST, instance=video)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": "success", "video_id": video_id, "memo": video.memo})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    return JsonResponse({"status": "invalid request"}, status=400)
