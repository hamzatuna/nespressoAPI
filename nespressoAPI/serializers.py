from rest_framework import serializers
from .models import (
    Sales,
    Machines,
    Personnels,
    Managers,
    Supervisors,
    Locations,
    TastingInformations,
    IntensiveHours,
    MachineConditions,
    User,
    PersonnelLocation)
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework.validators import UniqueValidator

# UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, max_length=128)
    email = serializers.EmailField(
        allow_blank=False, 
        label='Email address', 
        max_length=254, 
        required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=validated_data['is_active'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    def validate(self, data):
         # here data has all the fields which have validated values
         # so we can create a User instance out of it
         user = User(**data)

         # get the password from the data
         password = data.get('password')

         errors = dict()
         try:
             # validate the password and catch the exception
             validators.validate_password(password=password, user=User)

         # the exception raised here is different than serializers.ValidationError
         except exceptions.ValidationError as e:
             errors['password'] = list(e.messages)

         if errors:
             raise serializers.ValidationError(errors)

         return super(UserSerializer, self).validate(data)

    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password',
            'is_active',
            'user_type'
        )
class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Locations
        fields = '__all__'

class PersonnelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Personnels
        fields = (
            'name', 
            'wage',
            'phone_number',
            'user',
            'location_id')
    
    def create(self,  validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = User.objects.create(**user_data)
            return Personnels.objects.create(user=user, **validated_data)


class SalesSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Sales.objects.create(**validated_data)
    class Meta:
        model=Sales
        exclude = ()

#
#class AdminSalesSerializer(serializers.ModelSerializer):

#


class MachinesSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Machines.objects.create(**validated_data)
    class Meta:
        model=Machines
        exclude=()

class TastingInformationsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return TastingInformations.objects.create(**validated_data)
    class Meta:
        model = TastingInformations
        exclude=()