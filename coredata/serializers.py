from dataclasses import fields
from rest_framework import serializers

from coredata.models import Region, District, Reference, User
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueTogetherValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_role', 'region_name']

class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = '__all__'

class ReferenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields =['name_ru','name_en','name_uz','val','potassium_val','phosphorus_val','nitrogen_val','code'] 

class AllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','last_name','first_name','email','region','district']


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username','last_name','first_name','email','password','district']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username':{'required': False},
            'password': {'required': True},
            'district': {'required': True}
        }

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'password', 'username', 'district', 'email', 'first_name', 'last_name','region']
        extra_kwargs = {
            'last_name': {'required': False},
            'first_name': {'required': False},
            'email': {'required': False},
            'region': {'required': False},
            'username': {'required': True},
            'password': {'required': True},
            'district': {'required': True}
        }
    


            
class ChangeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'password', 'username', 'district', 'email', 'first_name', 'last_name','region']
        extra_kwargs = {
            'last_name': {'required': False},
            'first_name': {'required': False},
            'email': {'required': False},
            'region': {'required': False},
            'username': {'required': False},
            'password': {'required': False},
            'district': {'required': False}
        }    