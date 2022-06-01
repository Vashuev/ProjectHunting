from django.conf import settings # new
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('dj_rest_auth.urls')),
    path('accounts/registration/',include('dj_rest_auth.registration.urls')),
    path('accounts/', include('accounts.urls')),

    path('api/', include('mprs.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
