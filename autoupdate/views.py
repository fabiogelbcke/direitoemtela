from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .utils import get_new_videos
from django.http import HttpResponse
from videos.models import Video
# Create your views here.

@staff_member_required
def update_videos(request):
    no_videos = get_new_videos()
    if no_videos < 0:
        return HttpResponse(str(-1 * no_videos) + ' videos baixados, mas erro ao enviar email')
    return HttpResponse(str(no_videos) + ' videos baixados')
