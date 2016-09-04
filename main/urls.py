from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
                       url(r'^sobre$', TemplateView.as_view(template_name='about.html'), name='about'),
)
