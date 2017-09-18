from django.conf.urls import url, include
import views

urlpatterns = [
    #url(
    #    r'^search/videos/(?P<query>).*/(?P<page>\d+)/$',
    #views.VideoSearchResultsView.as_view(),
    #    name='video_search_results_page'
    #    ),
    url(
        r'^search/videos/(?P<query>.*)/$',
        views.VideoSearchResultsView.as_view(),
        name='video_search_results_page'
    ),
    url(
        r'^search/courses/(?P<query>.*)/$',
        views.CourseSearchResultsView.as_view(),
        name='course_search_results_page'
    ),
    url(
        r'^search/(?P<query>.*)/$',
        views.SearchResultsView.as_view(),
        name='search_results_page'
    ),
    url(
        r'^getsearch$',
        views.get_search_page,
        name='get_search_page'
    )
]
