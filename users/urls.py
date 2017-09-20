from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from .auth_shenanigans import logout_function
from .registration import register

urlpatterns = [
    url(r'^logout$', logout_function, name='logout'),
    url(r'^register$', register, name='register'),
    url(r'^account$',
        TemplateView.as_view(template_name='account.djhtml'),
        name='account'),
                            
]
