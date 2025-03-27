from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from . import serializers

User = get_user_model()

# Only focus on create accounts
class AccountCreate(generics.CreateAPIView): # CreateAPIView
     name = 'account-create'
     serializer_class = serializers.AccountSerializer


# Provides a list of users
class UserList(generics.ListCreateAPIView):
     name = 'user-list'
     permission_classes = (
          permissions.IsAuthenticated,
     )
     serializer_class = serializers.UserSerializer
     queryset = User.objects.all()

     def perform_create(self, serializer):
         company_id = self.request.user.company_id
         serializer.save(company_id=company_id)

    # overrides return only the results related to the company
     def get_queryset(self):
          # ensure taht the users belong to the company of the user that is making the request
          company_id = self.request.user.company_id
          return super().get_queryset().filter(company_id=company_id)


# Provides a view for a single user 
class UserDetail(generics.RetrieveUpdateDestroyAPIView): # RetrieveUpdateDestroyAPIView
      name = 'user-detail'
      permission_classes = (
          permissions.IsAuthenticated,
     )
      serializer_class = serializers.UserSerializer
      queryset = User.objects.all()

      def get_queryset(self):
          company_id = self.request.user.company_id
          return super().get_queryset().filter(company_id=company_id)


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