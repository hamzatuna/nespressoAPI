from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from datetime import datetime
#from django.utils.timezone import now




class Managers(models.Model):
    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    #Meta sınıfı olmadan modeli migrate ettigimizde django appname_tablename şeklinde isimlendiriyor. Bunun önüne geçmek için Meta sınıfıyla tabloya isim veriyoruz.
    class Meta:
        db_table = "Managers"


class Locations(models.Model):
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    LocationName = models.CharField(max_length=1000)
    class Meta:
        db_table = "Locations"

class Personnels(models.Model):
    LocationId = models.ForeignKey(Locations,on_delete=models.CASCADE,db_column='LocationId',related_name='%(class)s_Location')

    # Hakkında konuşulmalı.
    RegisteredLocationLatitude = models.FloatField()
    RegisteredLocationLongtitude = models.FloatField()
    #

    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Birthday = models.DateField()
    PhoneNumber = models.CharField(max_length=30)
    Wage = models.DecimalField(max_digits=10,decimal_places=6)
    IsActive = models.BooleanField()    
    class Meta:
        db_table = "Personnels"


class Machines(models.Model):
    Name = models.CharField(max_length=200)
    SerialNumber = models.CharField(max_length=1000)
    Fee = models.DecimalField(max_digits=10,decimal_places=3) # max_digits noktadan sonrayla beraber toplam kaç sayı olabilir, decimal_places ise noktadan önceki ondalık kısımda max kaç sayı olabilir.
    class Meta:
        db_table = "Machines"

class Supervisors(models.Model):
    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    PhoneNumber = models.CharField(max_length=30)
    LocationId = models.ForeignKey(Locations,on_delete=models.CASCADE,related_name='%(class)s_Location')
    IsActive = models.BooleanField()
    class Meta:
        db_table = "Supervisors"
    
class Sales(models.Model):
    MachineId = models.ForeignKey(Machines,on_delete=models.CASCADE,db_column='MachineId',related_name='%(class)s_Machine')
    PersonnelId = models.ForeignKey(Personnels,on_delete=models.CASCADE,db_column='PersonnelId',related_name='%(class)s_Personnel')
    LocationId = models.ForeignKey(Locations,on_delete=models.CASCADE,db_column='LocationId',related_name='%(class)s_Location')
    #SerialNumber = models.CharField(max_length=1000) #Seri numarası tekrar eklemek gerekli mi düşün.
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
    IntensiveHour = models.CharField(max_length=100) #Veritabanında 12.00-14.00 şeklinde kayıtlı olacak.
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


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
