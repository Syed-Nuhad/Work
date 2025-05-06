from django.contrib import admin
from django.urls import path, include

from accounts.views import create_superuser_view
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('securelogin/', admin.site.urls),
    path('', views.home, name='home'),
    path('store/', include('store.urls')),
    path('cart/', include('carts.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('accounts/', include('accounts.urls')),
    path('run-migrate/', views.run_migrate),
    path('create-superuser/', create_superuser_view),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
