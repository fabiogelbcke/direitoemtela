from django.conf.urls import url, include
from .utils import (make_course_payment, check_promo_code_discount)
from .boleto import generate_boleto, payment_update


urlpatterns = [
    url(r'^paycourse/(?P<course_id>\d+)',
        make_course_payment,
        name='pay_course'
        ),
    url(r'^generateboleto/(?P<course_id>\d+)',
        generate_boleto,
        name='generate_boleto'
        ),
    url(r'^asaasupdate',
        payment_update,
        name='payment_update'
        ),
    url(r'checkpromocode/(?P<course_id>\d+)',
        check_promo_code_discount,
        name='check_promo_code'
        ),
]
