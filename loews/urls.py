from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = "Loews"
admin.site.site_title = "Loews Admin Portal"
admin.site.index_title = "Welcome to Loews Admin Portal"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("coreapp.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)