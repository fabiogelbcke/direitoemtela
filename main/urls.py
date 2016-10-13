from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from .views import IndexView

urlpatterns = patterns('',
                       url(r'^$', IndexView.as_view(), name='index'),
                       url(r'^sobre$', TemplateView.as_view(template_name='about.html'), name='about'),
                       url(r'^google449e81b63167a1b6.html', TemplateView.as_view(template_name='google449e81b63167a1b6.html'), name='google_webmaster'),
)
