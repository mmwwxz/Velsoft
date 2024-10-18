from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = 'product.views.custom_page_not_found_view'
handler500 = 'product.views.custom_server_error_view'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

