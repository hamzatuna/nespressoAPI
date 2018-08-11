from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver


class Managers(models.Model):

    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)

    # Meta sınıfı olmadan modeli migrate ettigimizde django appname_tablename 
    # şeklinde isimlendiriyor. Bunun önüne geçmek için Meta sınıfıyla tabloya 
    # isim veriyoruz.
    class Meta:
        db_table = "Managers"


class Locations(models.Model):

    Latitude = models.FloatField()
    Longtitude = models.FloatField()
    LocationName = models.CharField(max_length=1000)

    class Meta:
        db_table = "Locations"

class Personnels(models.Model):

    Location = models.ForeignKey(Locations,on_delete=models.CASCADE)
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

    # max_digits noktadan sonrayla beraber toplam kaç sayı olabilir, 
    # decimal_places ise noktadan önceki ondalık kısımda max kaç sayı olabilir.
    Fee = models.DecimalField(max_digits=10,decimal_places=3)

    class Meta:
        db_table = "Machines"

class Supervisors(models.Model):

    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    PhoneNumber = models.CharField(max_length=30)
    Location = models.ForeignKey(Locations,on_delete=models.CASCADE)
    IsActive = models.BooleanField()

    class Meta:
        db_table = "Supervisors"
    
class Sales(models.Model):

    Machine = models.ForeignKey(Machines,on_delete=models.CASCADE)
    Personnel = models.ForeignKey(Personnels,on_delete=models.CASCADE)
    SerialNumber = models.CharField(max_length=1000) #Seri numarası tekrar eklemek gerekli mi düşün.
    CustomerName = models.CharField(max_length=200)
    CustomerSurname = models.CharField(max_length=200)
    CustomerPhoneNumber = models.CharField(max_length=30)
    CustomerEmail = models.EmailField(max_length=200)
    IsCampaign = models.BooleanField()

    class Meta:
        db_table = "Sales"

# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)