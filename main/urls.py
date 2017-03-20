from django.conf.urls import url, include
from django.views.generic import TemplateView
from .views import IndexView, AboutView
from django.views.decorators.cache import cache_page

urlpatterns = [
               url(r'^$', cache_page(5*60*60)(IndexView.as_view()), name='index'),
               url(r'^sobre$', cache_page(5*60*60)(AboutView.as_view()), name='about'),
               url(r'^google449e81b63167a1b6.html', TemplateView.as_view(template_name='google449e81b63167a1b6.html'), name='google_webmaster'),
]
