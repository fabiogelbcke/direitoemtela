from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
import views
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_page

urlpatterns = patterns('',
                       url(r'^video/(?P<slug>\d+)$',
                           cache_page(5*60*60)(views.VideoView.as_view()),
                           name='video_page'),
)
