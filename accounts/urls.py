from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:pk>/', views.UserProfileRetrieveView.as_view(), name='profile_retrive'),
    path('profile/update/<int:pk>/', views.UserProfileUpdateView.as_view(), name='profile_update'),
]