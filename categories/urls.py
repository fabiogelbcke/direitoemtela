from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
import views

urlpatterns = patterns('',
                       url(r'^temas$', views.CategoriesListView.as_view(), name='categories'),
                       url(r'^category/(?P<category_id>\d+)/(?P<page>\d+)/$',
                           views.CategoryView.as_view(), name='category_page'),
                       url(r'^category/(?P<category_id>\d+)$',
                           views.CategoryView.as_view(), name='category_page'),
                       url(r'^category/(?P<category_id>\d+)/(?P<video_index>\d+)$',
                           views.CategoryVideoView.as_view(), name='category_video'),
                           
)
