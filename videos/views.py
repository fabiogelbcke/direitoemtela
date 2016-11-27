from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Video
from hitcount.views import HitCountDetailView
from django.conf import settings
from django.core.urlresolvers import reverse


class VideoView(HitCountDetailView):
    model = Video
    slug_field = 'id'
    context_object_name = 'video'
    template_name = 'video-page.djhtml'
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super(VideoView, self).get_context_data(**kwargs)
        context['suggestions'] = self.object.categories.all()
        context['video_url'] = settings.WEBSITE_URL[:-1]
        context['video_url'] += reverse('video_page', kwargs={'slug': self.kwargs['slug']})
        return context
# Create your views here.

