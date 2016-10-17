from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Video
from hitcount.views import HitCountDetailView


class VideoView(HitCountDetailView):
    model = Video
    slug_field = 'id'
    context_object_name = 'video'
    template_name = 'video-page.html'
    count_hit = True
# Create your views here.

