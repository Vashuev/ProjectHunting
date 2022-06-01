from django.urls import reverse_lazy
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer
from .models import CustomUser
from .permissions import IsCurrentUser

class UserProfileRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

class UserProfileUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCurrentUser]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
