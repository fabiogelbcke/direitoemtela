from django.conf.urls import patterns, url, include
import views


urlpatterns = patterns('',
                       url(r'^baixarnovosvideos$', views.update_videos, name='baixarnovosvideos'),
)
