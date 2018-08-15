from rest_framework import serializers
from .models import Sales,Machines,Personnels,Managers,Supervisors,Locations,TastingInformations,IntensiveHours,MachineConditions
from django.contrib.auth import get_user_model
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

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

class SalesSerializer(serializers.ModelSerializer):
    # PersonnelId = serializers.PrimaryKeyRelatedField(read_only=True)
    # MachineId = serializers.PrimaryKeyRelatedField(read_only=True)
    # #SerialNumber = serializers.CharField(max_length=1000) #Seri numarası tekrar eklemek gerekli mi düşün.
    # CustomerName = serializers.CharField(max_length=200)
    # CustomerSurname = serializers.CharField(max_length=200)
    # CustomerPhoneNumber = serializers.CharField(max_length=30)
    # CustomerEmail = serializers.EmailField(max_length=200)
    # IsCampaign = serializers.BooleanField()

    def create(self, validated_data):
        return Sales.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.SerialNumber = validated_data.get('SerialNumber',instance.SerialNumber)
    #     instance.CustomerName = validated_data.get('CustomerName',instance.CustomerName)
    #     instance.CustomerSurname = validated_data.get('CustomerSurname',instance.CustomerSurname)
    #     instance.CustomerPhoneNumber = validated_data.get('CustomerPhoneNumber',instance.CustomerPhoneNumber)
    #     instance.CustomerEmail = validated_data.get('CustomerEmail',instance.CustomerEmail)
    #     instance.IsCampaign = validated_data.get('IsCampaign',instance.IsCampaign)
    #     instance.save()
    #     return instance

    class Meta:
        model=Sales
        exclude = ()

class MachinesSerializer(serializers.ModelSerializer):
    # Name = serializers.CharField(max_length=200)
    # SerialNumber = serializers.CharField(max_length=1000)
    # Fee = serializers.DecimalField(max_digits=10,decimal_places=3) # max_digits noktadan sonrayla beraber toplam kaç sayı olabilir, decimal_places ise noktadan önceki ondalık kısımda max kaç sayı olabilir.

    def create(self, validated_data):
        return Machines.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     instance.Name=validated_data.get('Name',instance.Name)
    #     instance.SerialNumber = validated_data.get('SerialNumber',instance.SerialNumber)
    #     instance.Fee = validated_data.get('Fee', instance.Fee)
    class Meta:
        model=Machines
        exclude=()

class TastingInformationsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return TastingInformations.objects.create(**validated_data)

    class Meta:
        model = TastingInformations
        exclude=()