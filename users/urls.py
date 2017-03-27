from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from .auth_shenanigans import logout_function

urlpatterns = [
    url(r'^logout$', logout_function, name='logout'),
]
