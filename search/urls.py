from django.conf.urls import patterns, url, include
import views

urlpatterns = patterns('',
                       url(
                           r'^search/(?P<query>[\w\s]+)/(?P<page>\d+)/$',
                           views.SearchResultsView.as_view(),
                           name='search_results_page'
                       ),
                       url(
                           r'^search/(?P<query>[\w\s]+)/$',
                           views.SearchResultsView.as_view(),
                           name='search_results_page'
                       ),
                       url(
                           r'^getsearch$',
                           views.get_search_page,
                           name='get_search_page'
                       )
)
