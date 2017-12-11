from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls')),
    url(r'^', include('categories.urls')),
    url(r'^', include('mailing.urls')),
    url(r'^', include('videos.urls')),
    url(r'^', include('search.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include('autoupdate.urls')),
    url(r'^', include('courses.urls')),
    url(r'^', include('coursetests.urls')),
    url(r'^payment/', include('payments.urls')),
    url('', include('social_django.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
