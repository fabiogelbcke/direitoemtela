from django.conf.urls import url, include
import views

urlpatterns = [
               url(
                r'^search/(?P<query>).*/(?P<page>\d+)/$',
                views.SearchResultsView.as_view(),
                   name='search_results_page'
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
