# posts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Video
from .forms import VideoForm
from django.shortcuts import get_object_or_404

@login_required
def upload_video(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        video_file = request.FILES.get('video_file')
        thumbnail_file = request.FILES.get('thumbnail_file')

        if not latitude or not longitude or not video_file or not thumbnail_file:
            return render(request, 'upload_video.html', {
                'form': VideoForm(), 
                'error': '位置情報、動画ファイル、サムネイルファイルの全てが必要です。'
            })

        video_form = VideoForm(request.POST, request.FILES)
        if video_form.is_valid():
            video = video_form.save(commit=False)
            video.user = request.user
            video.latitude = float(latitude)
            video.longitude = float(longitude)
            video.video_file = video_file
            video.thumbnail_file = thumbnail_file
            video.save()
            return redirect('video_list')
    else:
        video_form = VideoForm()
    return render(request, 'upload_video.html', {'form': video_form})

def video_list(request):
    videos = Video.objects.all().order_by('-uploaded_at')
    return render(request, 'video_list.html', {'videos': videos})


# posts/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Video

def video_map(request):
    videos = Video.objects.all()
    video_data = []
    for video in videos:
        if video.latitude and video.longitude and video.thumbnail_file and video.video_file:
            avatar_url = video.user.profile.avatar.url if video.user.profile.avatar else '/media/avatars/default.png'
            video_data.append({
                'id': video.id,
                'latitude': video.latitude,
                'longitude': video.longitude,
                'thumbnail_url': video.thumbnail_file.url,
                'avatar_url': avatar_url,
                'username': video.user.username,
                'uploaded_at': video.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse(video_data, safe=False)

def video_map_page(request):
    return render(request, 'video_map.html')


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'video_detail.html', {'video': video})