from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Company

User = get_user_model()

# Serializes the user models
class UserSerializer(serializers.HyperlinkedModelSerializer):
     class Meta:
          model = User
          fields = (
               'url', 
               'id', 
               'username',
               'password'
          )

          # password field is never sent back to the client
          extra_kwargs = {
               'password' : {'write_only': True},
          }

          def create(self, validated_data):
              return User.objects.create_user(**validated_data)
          
          def update(self, instance, validated_data):
               updated = super().update(instance, validated_data)

               if 'password' in validated_data:  # overrides the update method
                   updated.set_password(validated_data['password'])
                   updated.save()
               return updated
          


# Serializes the company model
class CompanySerializer(serializers.HyperlinkedModelSerializer):
      class Meta:
           model = Company
           fields = ('id', 'name' , 'address') 


# 
class AccountSerializer(serializers.Serializer):
       # serializer that has two nested serializers

       company = CompanySerializer()
       user = UserSerializer()

       def create(self, validated_data):
           company_data = validated_data['company']
           user_data = validated_data ['user']

        # call CompanyManager method to create cthe company and the user
           company, user = Company.objects.create_account(
                company_name= company_data.get('name'),
                company_address= company_data.get('address'),
                username= user_data.get('username'),
                password= user_data.get('password'),
           )     

           return {'company' : company, 'user' : user}


       def update(self, instance, validated_data):
            raise NotImplementedError('Cannot call update() on an account')

