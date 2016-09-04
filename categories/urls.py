from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

urlpatterns = patterns('',
                       url(r'^temas$', TemplateView.as_view(template_name='categories.html'), name='categories'),
)
