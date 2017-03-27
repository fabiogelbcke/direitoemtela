from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from categories.models import Category
from apiclient.discovery import build
from django.conf import settings
from django.views.decorators.cache import cache_page
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.djhtml'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['featured_categories'] = Category.objects.filter(featured=True)
        return context

    #def dispatch(self, request, *args, **kwargs):
    #    if not request.user.is_authenticated():
    #        return redirect('under_construction')
    #    else:
    #        return super(IndexView, self).dispatch(request, *args, **kwargs)

class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        youtube = build(
        settings.YOUTUBE_API_SERVICE_NAME,
        settings.YOUTUBE_API_VERSION,
        developerKey=settings.YT_KEY)
        response = youtube.channels().list(
            id=settings.YT_CHANNEL_ID,
            part='id,statistics'
        ).execute()
        channel_info = response['items'][0]['statistics']
        context['total_views'] = "{:,}".format(int(channel_info['viewCount'])).replace(',', '.')
        context['subscribers'] = "{:,}".format(int(channel_info['subscriberCount'])).replace(',', '.')
        context['total_videos'] = channel_info['videoCount']
        return context
