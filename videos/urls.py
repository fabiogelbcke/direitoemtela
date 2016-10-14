from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',
                       url(r'^video/(?P<slug>\d+)$',
                           views.VideoView.as_view()
                           , name='video_page'),
)
