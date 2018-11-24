import logging
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework.validators import UniqueValidator
from django.contrib.auth.hashers import make_password

# UserModel = get_user_model()

class UsersSerializer(serializers.ModelSerializer):

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
             logging.error()
             raise serializers.ValidationError(errors)

         return super(UsersSerializer, self).validate(data)

    class Meta:
        model = User
        fields = (
            'id', #Yeni Ekledim 16 Kasim 2018-Fatih

            'username',
            'email',
            'password',
            'is_active',
            'user_type'
        )


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sales
        exclude=()



class LocationsSerializer(serializers.ModelSerializer):
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




class OldPersonnelsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Personnels.objects.create(**validated_data)
    class Meta:
        model=Personnels
        exclude=()



class PersonnelsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    location = LocationsSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(queryset = Locations.objects.all(),source='location',write_only=True)

    class Meta:
        model = Personnels
        exclude = ()

    def create(self, validated_data):
        with transaction.atomic():
            user_data = validated_data.pop('user')
            user = User(**user_data)
            user.set_password(user_data['password'])
            user.user_type = 2
            user.save()

            return Personnels.objects.create(user=user, **validated_data)

class SalesSerializer(serializers.ModelSerializer):
    #Read (Get)
    location = LocationsSerializer(read_only=True)
    personnel = PersonnelsSerializer(read_only=True)
    machine = MachinesSerializer(read_only=True)

    # Write (Post)
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset = Machines.objects.all(),
        source='machine',
        write_only=True)
    personnel_id = serializers.PrimaryKeyRelatedField(
        queryset = Personnels.objects.all(),
        source='personnel',
        write_only=True)


    def create(self, validated_data):
        personnel = Personnels.objects.get(pk=validated_data['personnel'])

        # personel yoksa hata don
        if not personnel:
            logging.error('satis ekleme gonderilen personel_id bulunamadi')
            raise serializers.ValidationError('Personel bulunamadi')

        location = personnel.location
        user = self.context['request'].user

        # baskasinin yerine satis eklenemez
        if not personnel.user==user:
            logging.error('satis eklerken personnel_id uyusmazligi yasandi')
            raise serializers.ValidationError('farkli kullanici icin eklenmeye calisildi')

        # location yoksa hata don
        if not location:
            logging.error('lokasyonu eklenmeyen personle satis eklemeye calisti')
            raise serializers.ValidationError('lokasyon bulunamadi')

        # signallerden gelen hatalari yakalamak icin
        try: 
            sale = Sales.objects.create(
                **validated_data,
                location=location)
            return sale

        except Exception as e:
            logging.error('satis eklerken validation hatasi %s', e)
            raise serializers.ValidationError(e.message)

    class Meta:
        model = Sales
        exclude = ()
        read_only_fields = ('date',)

class IntensiveHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=IntensiveHours
        exclude=()
class CustomerGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerGoals
        exclude=()

class TastingInformationsSerializer(serializers.ModelSerializer):
    location = LocationsSerializer(many=False,required=True)
    machine_condition = MachineConditionsSerializer(many=False,required=True)
    intensive_hour = IntensiveHoursSerializer(many=False,required=True)
    personnel = PersonnelsSerializer(many=False,required=True)

    #def create(self, validated_data):
    #    return TastingInformations.objects.create(**validated_data)
    class Meta:
        model=TastingInformations
        exclude=()

class StockSerializer(serializers.ModelSerializer):

    machine = MachinesSerializer(read_only=True)
    machine_id = serializers.PrimaryKeyRelatedField(
        queryset = Machines.objects.all(),
        source='machine',
        write_only=True)

    def create(self, validated_data):
        user = self.context['request'].user
        
        # personnelse lokasyonu kullanma
        if user.user_type==2:
            validated_data['location'] = user.personnels.location
        
        location = validated_data['location']
        machine = validated_data['machine']
        stock_count = validated_data['stock_count']

        stock, created = Stock.objects.get_or_create(
            machine=machine, 
            location=location, 
            defaults={
                'stock_count': stock_count,
                'user': user})
        
        # stock varsa uzerine ekle
        if not created:
            stock.stock_count +=stock_count
            stock.save()

        return stock

    class Meta:
        model = Stock
        exclude = ('user',)
        read_only_fields = ('location',)
