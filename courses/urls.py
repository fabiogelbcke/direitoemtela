from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from .views import CourseView

urlpatterns = [
    url(r'^course/(?P<slug>\d+)$', CourseView.as_view()),
]
