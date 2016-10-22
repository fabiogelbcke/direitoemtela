from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
import views
from django.views.decorators.cache import cache_page

urlpatterns = patterns('',
                       url(r'^temas$',
                           cache_page(24*60*60)(views.CategoriesListView.as_view()),
                           name='categories'),
                       url(r'^category/(?P<category_id>\d+)/(?P<page>\d+)/$',
                           cache_page(5*60*60)(views.CategoryView.as_view()),
                           name='category_page'),
                       url(r'^category/(?P<category_id>\d+)$',
                           cache_page(5*60*60)(views.CategoryView.as_view()),
                           name='category_page'),
                       url(r'^category/(?P<category_id>\d+)/(?P<video_index>\d+)$',
                           cache_page(5*60*60)(views.CategoryVideoView.as_view()),
                           name='category_video'),
                           
)
