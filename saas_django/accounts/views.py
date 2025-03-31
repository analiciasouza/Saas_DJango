from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions

from core.views import CompanySafeViewMaxin
from . import serializers

User = get_user_model()

# Only focus on create accounts
class AccountCreate(generics.CreateAPIView): # CreateAPIView
     name = 'account-create'
     serializer_class = serializers.AccountSerializer


# Provides a list of users
class UserList( CompanySafeViewMaxin, generics.ListCreateAPIView):
     name = 'user-list'
     permission_classes = (
          permissions.IsAuthenticated,
     )
     serializer_class = serializers.UserSerializer
     queryset = User.objects.all()


# Provides a view for a single user 
class UserDetail(CompanySafeViewMaxin, generics.RetrieveUpdateDestroyAPIView): # RetrieveUpdateDestroyAPIView
      name = 'user-detail'
      permission_classes = (
          permissions.IsAuthenticated,
     )
      serializer_class = serializers.UserSerializer
      queryset = User.objects.all()



# Provides the detailed view of a company 
class CompanyDetail(generics.RetrieveUpdateAPIView):
      name = 'company-detail'
      permission_classes = (
          permissions.IsAuthenticated,
     )
      serializer_class = serializers.CompanySerializer

      def get_object(self):
          # ensure that users can only see the company that they belong to
          return self.request.user.company