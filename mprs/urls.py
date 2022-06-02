from graphene_file_upload.django import FileUploadGraphQLView
from django.urls import path
from . import views
from mprs.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema))),
]