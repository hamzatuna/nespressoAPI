import re
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
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
    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)

    # foreign keys
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    # Meta sınıfı olmadan modeli migrate ettigimizde
    #  django appname_tablename şeklinde isimlendiriyor.
    # Bunun önüne geçmek için Meta sınıfıyla tabloya isim veriyoruz.
    class Meta:
        db_table = "Managers"

class Machines(models.Model):
    Name = models.CharField(max_length=200)
    #SerialNumber = models.CharField(max_length=1000)

    # max_digits noktadan sonrayla beraber toplam kaç sayı olabilir,
    # decimal_places ise noktadan önceki ondalık kısımda max kaç sayı olabilir.
    Fee = models.DecimalField(max_digits=10,decimal_places=3)

    class Meta:
        db_table = "Machines"

class Locations(models.Model):
    Latitude = models.FloatField(null=True)
    Longitude = models.FloatField(null=True)
    LocationName = models.CharField(max_length=1000)
    stock = models.IntegerField(default=0)

    class Meta:
        db_table = "Locations"

class LocationHistory(models.Model):
    stock = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now,blank=True)

    # foreign keys
    location_id = models.ForeignKey(
        Locations,
        on_delete=models.CASCADE,
        db_column='LocationId',
        null=True)

class Personnels(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    birthday = models.DateField(null=True)
    phone_number = models.CharField(max_length=30, null=True)
    wage = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    # foreign keys
    location_id = models.ForeignKey(
        Locations,
        on_delete=models.CASCADE,
        db_column='LocationId',
        null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = "Personnels"

class PersonnelLocation(models.Model):

    #foreign keys
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    location = models.OneToOneField(Locations, on_delete=models.CASCADE)

class Supervisors(models.Model):
    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    PhoneNumber = models.CharField(max_length=30)
    IsActive = models.BooleanField()

    # foreign keys
    Location = models.ForeignKey(Locations,on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = "Supervisors"
    
class Sales(models.Model):
    MachineId = models.ForeignKey(Machines,on_delete=models.CASCADE,db_column='MachineId',related_name='%(class)s_Machine')
    PersonnelId = models.ForeignKey(Personnels,on_delete=models.CASCADE,db_column='PersonnelId',related_name='%(class)s_Personnel')
    LocationId = models.ForeignKey(
        Locations,
        on_delete=models.CASCADE,
        db_column='LocationId',
        null=True,
        related_name='%(class)s_Location')
    SerialNumber = models.CharField(max_length=1000)
    Date = models.DateTimeField(default=datetime.now,blank=True)
    CustomerName = models.CharField(max_length=200)
    CustomerSurname = models.CharField(max_length=200)
    CustomerPhoneNumber = models.CharField(max_length=30)
    CustomerEmail = models.EmailField(max_length=200)
    IsCampaign = models.BooleanField()
    class Meta:
        db_table = "Sales"

#Yoğun saatler tablosu
class IntensiveHours(models.Model):
    #Veritabanında 12.00-14.00 şeklinde kayıtlı olacak.
    IntensiveHour = models.CharField(max_length=100)

    class Meta:
        db_table = "IntensiveHours"

class MachineConditions(models.Model):
    MachineCondition = models.CharField(max_length=300)

    class Meta:
        db_table = "MachineConditions"


class TastingInformations(models.Model):
    PersonnelId = models.ForeignKey(Personnels,on_delete=models.CASCADE,db_column='PersonnelId',related_name='%(class)s_Personnel')
    MachineConditionId = models.ForeignKey(MachineConditions,on_delete=models.CASCADE,db_column='MachineConditionId',related_name='%(class)s_MachineCondition')
    IntensiveHourId = models.ForeignKey(IntensiveHours,on_delete=models.CASCADE,db_column='IntensiveHourId',related_name='%(class)s_IntensiveHour')
    Date = models.DateTimeField(default=datetime.now,blank=True)
    LocationId = models.ForeignKey(Locations, on_delete=models.CASCADE, db_column='LocationId',related_name='%(class)s_Location')
    TotalEspressoRecipe = models.IntegerField() #Yapılan toplam espresso tarif
    TotalMilkyRecipe = models.IntegerField() #Yapılan toplam sütlü tarif
    DailyCoffeeConsumption = models.IntegerField() #Günlük tüketilen kahve adedi
    DailyShopCoffeeConsumption = models.IntegerField() #Günlük mağazanın kullandığı kahve adeti
    DailyMilkBoxConsumption = models.IntegerField() #Günlük kullanılan süt (kutu)
    class Meta:
        db_table = "TastingInformations"

class CustomerGoals(models.Model):
    sale_goal = models.IntegerField()
    date = models.DateField(unique=True, validators=[month_validator])
    
    # foreign keys
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# Location updatelendiginde eski degerini tutacak olan tablo
@receiver(post_save, sender=Locations)
def log_stocks(sender, instance=None, created=False, **kwargs):
    LocationHistory.objects.create(location_id=instance, stock=instance.stock)

# satis eklendiginde otamatik stoktan dusme
@receiver(post_save, sender=Sales)
def decrease_stock(sender, instance=None, created=False, **kwargs):
    if created:
        location = instance.LocationId
        if location:
            location.stock -=1
            location.save()

