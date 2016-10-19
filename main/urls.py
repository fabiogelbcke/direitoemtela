from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from .views import IndexView, AboutView
from django.views.decorators.cache import cache_page

urlpatterns = patterns('',
                       url(r'^$', cache_page(0*60)(IndexView.as_view()), name='index'),
                       url(r'^sobre$', cache_page(60*60)(AboutView.as_view()), name='about'),
                       url(r'^google449e81b63167a1b6.html', TemplateView.as_view(template_name='google449e81b63167a1b6.html'), name='google_webmaster'),
)
