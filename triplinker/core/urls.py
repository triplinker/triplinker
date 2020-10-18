import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('accounts.urls')),
    path('feed/', include('feed.urls')),
    path('messages/', include('chat.urls')),
    path('places/', include('trip_places.urls')),
    path('journeys/', include('journeys.urls')),
    path('recommendations/', include('recommendations.urls')),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns.append(path('debug/', include(debug_toolbar.urls)))
