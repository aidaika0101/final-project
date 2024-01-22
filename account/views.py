from dj_rest_auth.views import LogoutView
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from . import serializers
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer


class UserRegisterView(generics.CreateAPIView):

    serializer_class = serializers.RegisterSerializer

class CustomLogoutView(LogoutView):
    permission_classes = (permissions.IsAuthenticated,)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserListSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)





