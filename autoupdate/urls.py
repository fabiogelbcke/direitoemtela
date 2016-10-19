from django.conf.urls import patterns, url, include
import views, utils
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^baixarnovosvideos$', views.update_videos, name='baixarnovosvideos'),
                       url(r'^adicionarvideo$',
                           staff_member_required(
                               TemplateView.as_view(template_name='addvideo.html')),
                           name='add_video_by_id'),
                       url(r'^getvideobyid$',
                           utils.get_video_by_id,
                           name='get_video_by_id'),
)
