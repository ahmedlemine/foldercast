from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import directory_list, create_feed, feed_details, clean_up, app_settings

app_name = 'feeds'

urlpatterns = [
    path("", directory_list, name="directory_list"),
    path("feed/create/<str:directory_name>/", create_feed, name="create_feed"),
    path("feed/details/<str:feed_uuid>/", feed_details, name="feed_details"),
    path("feed/settings/", app_settings, name="settings"),
    path("feed/settings/cleanup/", clean_up, name="cleanup"),
]

    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static('library/', document_root="library/")
