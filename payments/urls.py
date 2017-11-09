from django.conf.urls import url, include
from .utils import make_course_payment, register_with_promo_code
from .boleto import generate_boleto, payment_update


urlpatterns = [
    url(r'^paycourse/(?P<course_id>\d+)',
        make_course_payment,
        name='pay_course'
        ),
    url(r'^promoregister/(?P<course_id>\d+)',
        register_with_promo_code,
        name='register_promo_code'
        ),
    url(r'^generateboleto/(?P<course_id>\d+)',
        generate_boleto,
        name='generate_boleto'
        ),
    url(r'^asaasupdate',
        payment_update,
        name='payment_update'
        )
]
