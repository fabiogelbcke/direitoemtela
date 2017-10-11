from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from .auth_shenanigans import logout_function
from .registration import register
from .views import account_page
from .utils import (update_user_info, change_password,
                    upload_new_photo)

urlpatterns = [
    url(
        r'^logout$',
        logout_function,
        name='logout'
    ),
    url(
        r'^register$',
        register,
        name='register'
    ),
    url(
        r'^account$',
        account_page,
        name='account'
    ),
    url(
        r'^changepwd$',
        change_password,
        name='change_password'
    ),
    url(
        r'^updateuser$',
        update_user_info,
        name='update_user_info'
    ),
    url(
        r'^uploadphoto$',
        upload_new_photo,
        name='upload_new_photo'
    ),
]
