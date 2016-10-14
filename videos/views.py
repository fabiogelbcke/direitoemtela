from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Video

class VideoView(DetailView):
    model = Video
    slug_field = 'id'
    context_object_name = 'video'
    template_name = 'video-page.html'
# Create your views here.
