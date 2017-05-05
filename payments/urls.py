from django.conf.urls import url, include
from .utils import make_course_payment

urlpatterns = [
    url(r'^paycourse/(?P<course_id>\d+)',
        make_course_payment,
        name='pay_course'
        ),
]
