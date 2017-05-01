from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from .views import (CourseView, dashboard_courses, CourseItemView,
                    CourseProgressView)
from .utils import set_item_done


urlpatterns = [
    url(r'^course/(?P<slug>\d+)$',
        CourseView.as_view(),
        name='course_page'),
    url(r'^course/(?P<slug>\d+)/progress$',
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
    url(r'^setitemdone/(?P<item_id>\d+)$',
        set_item_done,
        name='set_item_done'),
]
