from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from .views import (CourseView, dashboard_courses, CourseItemView,
                    CourseProgressView, CertificateView, CertificatePDFView,
                    CertificatePDFHTML, CertificatePDF)
from .utils import set_item_done
from .generate_certificate import send_pdf_email


urlpatterns = [
    url(r'^course/(?P<course_id>\d+)$',
        CourseView.as_view(),
        name='course_page'),
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
    url(r'^certificatepdf/(?P<identifier>\w+)$',
        CertificatePDFView.as_view(),
        name='certificate_pdf'),
    url(r'^certificatehtml/(?P<identifier>\w+)$',
        CertificatePDFHTML.as_view(),
        name='certificate_html'),
    url(r'^attcer/(?P<identifier>\w+)$',
        CertificatePDF.as_view(),
        name='certficate_attempt'),
    url(r'^sendpdf$',
        send_pdf_email,
        name= 'send_pdf'),
    url(r'^setitemdone/(?P<item_id>\d+)$',
        set_item_done,
        name='set_item_done'),
]
