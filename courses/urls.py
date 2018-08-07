from django.conf.urls import url, include
from django.views.generic import TemplateView

from .views import (CourseView, dashboard_courses, CourseItemView,
                    CourseProgressView, CertificateView, CertificatePrint,
                    CoursePaymentView, CertificateWithContentPrint)
from .utils import (set_item_done, admin_register_to_course,
                    admin_unregister_from_course)
from .generate_certificate import send_pdf_email


urlpatterns = [
    url(r'^course/(?P<course_id>\d+)$',
        CourseView.as_view(),
        name='course_page'),
    url(r'^coursepay/(?P<course_id>\d+)$',
        CoursePaymentView.as_view(),
        name='course_payment_page'),
    url(r'^course/progress/(?P<course_id>\d+)$',
        CourseProgressView.as_view(),
        name='course_progress'),
    url(r'^dashboardcourses$',
        dashboard_courses,
        name= 'dashboard_courses'),
    url(r'^course/(?P<course_id>\d+)/(?P<position>\d+)$',
        CourseItemView.as_view(),
        name='course_item'),
    url(r'^course/(?P<course_id>\d+)/(?P<position>\d+)/(?P<question_no>\d+)$',
        CourseItemView.as_view(),
        name='course_item'),
    url(r'^certificate/(?P<identifier>\w+)$',
        CertificateView.as_view(),
        name='certificate_view'),
    url(r'^printcertificate/(?P<identifier>\w+)$',
        CertificatePrint.as_view(),
        name='print_certificate'),
    url(r'^printcertificatewithcontent/(?P<identifier>\w+)$',
        CertificateWithContentPrint.as_view(),
        name='print_certificate_with_content'),
    url(r'^setitemdone/(?P<item_id>\d+)$',
        set_item_done,
        name='set_item_done'),
    url(r'^course/adminunregister/(?P<course_id>\d+)$',
        admin_unregister_from_course,
        name='admin_unregister_from_course'),
    url(r'^course/adminregister/(?P<course_id>\d+)$',
        admin_register_to_course,
        name='admin_register_to_course'),
]
