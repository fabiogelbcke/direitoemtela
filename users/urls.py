from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page

from .auth_shenanigans import (logout_function, email_login,
                               send_password_reset_email)
from .registration import register
from .views import account_page, CustomPasswordResetView
from .utils import (update_user_info, change_password,
                    upload_new_photo, save_cropped_photo,
                    reset_password_confirm)

urlpatterns = [
    url(
        r'^email_login$',
        email_login,
        name='email_login'
    ),
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
        r'^resetarsenha/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
        CustomPasswordResetView.as_view(),
        name='password_reset_view'
    ),
    url(
        r'^pwresetemail$',
        send_password_reset_email,
        name='send_password_reset_email'
    ),
    url(
        r'^pwresetconfirmed$',
        TemplateView.as_view(template_name='password-reset-done-page.djhtml'),
        name='password_reset_done'
    ),
    url(
        r'^conta$',
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
    url(
        r'^savecroppedphoto$',
        save_cropped_photo,
        name='save_cropped_photo'
    ),
    url(
        r'^rstpasswordconfirm$',
        reset_password_confirm,
        name='reset_password_confirm'
    ),
]
