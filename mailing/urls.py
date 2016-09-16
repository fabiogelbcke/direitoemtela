from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^emconstrucao$', TemplateView.as_view(template_name='site-em-construcao.html'), name='under_construction'),
)
