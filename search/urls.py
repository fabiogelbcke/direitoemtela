from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
                       url(r'^search/(?P<query>\w+)/(?P<page>\d+)/$',
                        views.SearchResultsView.as_view(), name='search_results_page'),
                       url(r'^search/(?P<query>\w+)/$',
                        views.SearchResultsView.as_view(), name='search_results_page'),
)
