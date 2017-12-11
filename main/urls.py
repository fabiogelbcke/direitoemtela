from django.conf.urls import url, include
from django.views.generic import TemplateView
from .views import IndexView, AboutView, LoginView
from django.views.decorators.cache import cache_page

urlpatterns = [
    url(
        r'^$',
        IndexView.as_view(),
        name='index'
    ),
    url(
        r'^login$',
        LoginView.as_view(),
        name='login'
    ),
    url(
        r'^sobre$',
        AboutView.as_view(),
        name='about'
    ),
    url(
        r'^google449e81b63167a1b6.html',
        TemplateView.as_view(template_name='google449e81b63167a1b6.html'),
        name='google_webmaster'
    ),
    url(
        r'^robots.txt$',
        TemplateView.as_view(template_name="robots.txt",content_type="text/plain")
    )
]
