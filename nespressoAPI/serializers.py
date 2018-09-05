from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
import logging

UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, max_length=128)
    email = serializers.EmailField(allow_blank=False, label='Email address', max_length=254, required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            is_active=validated_data['is_active']
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
        model = UserModel
        fields = ('username', 'email', 'password','is_active')

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sales
        exclude=()

class LocationSerializer(serializers.ModelSerializer):
    def create(self,validated_data):
        return Locations.objects.create(**validated_data)
    class Meta:
        model=Locations
        exclude=()

class MachineConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=MachineConditions
        exclude=()

class MachinesSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Machines.objects.create(**validated_data)
    class Meta:
        model=Machines
        exclude=()


class PersonnelsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Personnels.objects.create(**validated_data)
    class Meta:
        model=Personnels
        exclude=()


class SalesSerializer(serializers.ModelSerializer):
    #Serializer Constructoru içerisine örneğin source='LocationId' ekleyip,serializer'dan
    #dönen field'ın ismini Location olarak değiştirebiliyoruz. Bu durumda API oluşturduğu
    #JSON içerisinde LocationId değil Location başlığı veriyor. Bununla beraber datatables
    #ajax requesti bu yeniden isimlendirme olayına sıkıntı çıkardığı için field'ları Sales
    #tablosundaki asli isimleriyle yolluyoruz.
    LocationId = LocationSerializer(many=False,required=True)
    MachineId = MachinesSerializer(many=False,required=True)
    PersonnelId =PersonnelsSerializer(many=False,required=True)

    class Meta:
        model=Sales
        exclude=()


class IntensiveHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=IntensiveHours
        exclude=()

class TastingInformationsSerializer(serializers.ModelSerializer):
    LocationId = LocationSerializer(many=False,required=True)
    MachineConditionId = MachineConditionsSerializer(many=False,required=True)
    IntensiveHourId = IntensiveHoursSerializer(many=False,required=True)
    PersonnelId = PersonnelsSerializer(many=False,required=True)

    #def create(self, validated_data):
    #    return TastingInformations.objects.create(**validated_data)
    class Meta:
        model=TastingInformations
        exclude=()


