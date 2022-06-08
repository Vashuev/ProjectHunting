from django.conf import settings # new
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from graphene_file_upload.django import FileUploadGraphQLView
from django.views.decorators.csrf import csrf_exempt
from .scheme import schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', csrf_exempt(include('dj_rest_auth.urls'))),
    path('accounts/registration/',include('dj_rest_auth.registration.urls')),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema))),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
