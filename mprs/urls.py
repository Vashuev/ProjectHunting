from graphene_django.views import GraphQLView
from django.urls import path
from . import views
from mprs.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('graph/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]