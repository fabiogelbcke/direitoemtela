from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .utils import get_new_videos
from django.http import HttpResponse
# Create your views here.

@staff_member_required
def update_videos(request):
    no_videos = get_new_videos()
    return HttpResponse(str(no_videos) + ' videos baixados')

