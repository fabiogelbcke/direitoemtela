from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
import views
from django.contrib.admin.views.decorators import staff_member_required
urlpatterns = patterns('',
                       url(r'^video/(?P<slug>\d+)$',
                           views.VideoView.as_view()
                           , name='video_page'),
)
