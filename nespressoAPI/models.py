import re
import operator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from datetime import datetime
from django.contrib.auth.hashers import make_password
from .validators import month_validator


class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )

        print(password)
        user.set_password(make_password(password))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Manager'),
        (2, 'Personnel'),
        (3, 'Supervisor')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



class Managers(models.Model):
    #fields
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)

    #foreign keys
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)



class Machines(models.Model):
    #fields
    name = models.CharField(max_length=200, unique=True)



class Locations(models.Model):
    #fields
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    location_name = models.CharField(max_length=1000)



class Personnels(models.Model):
    #fields
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    birthday = models.DateField(null=True)
    phone_number = models.CharField(max_length=30, null=True)
    wage = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    tc_no = models.FloatField(validators=[MinValueValidator(1e10), MaxValueValidator(1e11-1)])
    
    #foreign keys
    location_id = models.ForeignKey(
        Locations,
        db_column='location_id',
        on_delete=models.CASCADE,
        null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)



class PersonnelLocation(models.Model):
    #foreign keys
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location_id = models.OneToOneField(Locations,db_column='location_id', on_delete=models.CASCADE)



class Supervisors(models.Model):
    #fields
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=30)
    is_active = models.BooleanField()

    #foreign keys
    location_id = models.ForeignKey(Locations,db_column='location_id',on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)



class Sales(models.Model):
    #fields
    date = models.DateTimeField(default=datetime.now,blank=True)
    customer_name = models.CharField(max_length=200)
    customer_surname = models.CharField(max_length=200)
    custome_phone_number = models.CharField(max_length=30)
    customer_email = models.EmailField(max_length=200)
    is_campaign = models.BooleanField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    price = models.DecimalField(max_digits=10,decimal_places=3)
    serial_number = models.CharField(max_length=1000)

    #foreign keys
    machine_id = models.ForeignKey(Machines,db_column='machine_id',on_delete=models.CASCADE,related_name='%(class)s_Machine')
    personnel_id = models.ForeignKey(Personnels,db_column='personnel_id',on_delete=models.CASCADE,related_name='%(class)s_Personnel')
    location_id = models.ForeignKey(
        Locations,
        db_column='location_id',
        on_delete=models.CASCADE,
        null=True,
        related_name='%(class)s_Location')



#Yoğun saatler tablosu
class IntensiveHours(models.Model):
    #fields
    #Veritabanında 12.00-14.00 şeklinde saat aralıkları şeklinde kayıtlı olacak.
    intensive_hour = models.CharField(max_length=100)



class MachineConditions(models.Model):
    #fields
    machine_condition = models.CharField(max_length=300)



class TastingInformations(models.Model):
    #fields
    date = models.DateTimeField(default=datetime.now,blank=True)
    total_espresso_recipe = models.IntegerField() #Yapılan toplam espresso tarif
    total_milky_recipe = models.IntegerField() #Yapılan toplam sütlü tarif
    daily_coffee_consumption = models.IntegerField() #Günlük tüketilen kahve adedi
    daily_shop_coffee_consumption = models.IntegerField() #Günlük mağazanın kullandığı kahve adeti
    daily_milk_box_consumption = models.IntegerField() #Günlük kullanılan süt (kutu)

    #foreign keys
    personnel_id = models.ForeignKey(Personnels,db_column='personnel_id',on_delete=models.CASCADE,related_name='%(class)s_Personnel')
    machine_condition_id = models.ForeignKey(MachineConditions,db_column='machine_condition_id',on_delete=models.CASCADE,related_name='%(class)s_MachineCondition')
    intensive_hour_id = models.ForeignKey(IntensiveHours,db_column='intensive_hour_id',on_delete=models.CASCADE,related_name='%(class)s_IntensiveHour')
    location_id = models.ForeignKey(Locations,db_column='location_id', on_delete=models.CASCADE,related_name='%(class)s_Location')



class CustomerGoals(models.Model):
    #fields
    sale_goal = models.IntegerField()
    date = models.DateField(unique=True, validators=[month_validator])
    
    #foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class Stock(models.Model):
    #fields
    stock_count = models.IntegerField(default=0)

    #foreign keys
    machine_id = models.ForeignKey(Machines, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



class StockHistory(models.Model):
    #fields
    stock_count = models.IntegerField(default=0)
    date = models.DateField(default=datetime.now)
    note = models.CharField(max_length=15)

    #foreign keys
    machine = models.ForeignKey(Machines, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)



# Stock updatelendiginde eski degerini tutacak olan tablo
@receiver(post_save, sender=Stock)
def log_stocks(sender, instance=None, created=False, **kwargs):
    fields = [
        'machine',
        'location',
        'user',
        'stock_count'
    ]
    stock = {field:getattr(instance, field)  for field in fields}
    StockHistory.objects.create(
        note = 'created' if created else 'updated',
        **stock
    )



# # satis eklendiginde otamatik stoktan dusme
# @receiver(post_save, sender=Sales)
# def decrease_stock(sender, instance=None, created=False, **kwargs):
#     if created:
#         location = instance.location_id
#         if location:
#             location.stock -=1
#             location.save()

