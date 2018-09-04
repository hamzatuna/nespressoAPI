from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Manager'),
        (2, 'Personnel'),
        (3, 'Supervisor')
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)


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


class Locations(models.Model):
    Latitude = models.FloatField()
    Longtitude = models.FloatField()
    LocationName = models.CharField(max_length=1000)
    
    class Meta:
        db_table = "Locations"

class Personnels(models.Model):
    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    Email = models.EmailField(max_length=200)
    Birthday = models.DateField()
    PhoneNumber = models.CharField(max_length=30)
    Wage = models.DecimalField(max_digits=10,decimal_places=6)
    IsActive = models.BooleanField()

    # foreign keys
    LocationId = models.ForeignKey(
        Locations, 
        on_delete=models.CASCADE,
        db_column='LocationId')
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

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
    IsActive = models.BooleanField()
    
    # foreign keys
    Location = models.ForeignKey(Locations,on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    class Meta:
        db_table = "Supervisors"
    
class Sales(models.Model):
   # SerialNumber = models.CharField(max_length=1000) 
   # Seri numarası tekrar eklemek gerekli mi düşün.
    CustomerName = models.CharField(max_length=200)
    CustomerSurname = models.CharField(max_length=200)
    CustomerPhoneNumber = models.CharField(max_length=30)
    CustomerEmail = models.EmailField(max_length=200)
    IsCampaign = models.BooleanField()

    # foreign keys
    MachineId = models.ForeignKey(
        Machines,
        on_delete=models.CASCADE,
        db_column='MachineId')
    PersonnelId = models.ForeignKey(
        Personnels,
        on_delete=models.CASCADE,
        db_column='PersonnelId')
 
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
    TotalEspressoRecipe = models.IntegerField() #Yapılan toplam espresso tarif
    TotalMilkyRecipe = models.IntegerField() #Yapılan toplam sütlü tarif
    DailyCoffeeComsumption = models.IntegerField() #Günlük tüketilen kahve adedi
    DailyShopCoffeeConsumption = models.IntegerField() #Günlük mağazanın kullandığı kahve adeti
    DailyMilkBoxConsumption = models.IntegerField() #Günlük kullanılan süt (kutu)
    
    # foreign keys
    PersonnelId = models.ForeignKey(
        Personnels,
        on_delete=models.CASCADE,
        db_column='PersonnelId')
    MachineConditionId = models.ForeignKey(
        MachineConditions,
        on_delete=models.CASCADE,
        db_column='MachineConditionId')
    IntensiveHoursId = models.ForeignKey(
        IntensiveHours,
        on_delete=models.CASCADE,
        db_column='IntensiveHoursId')

    class Meta:
        db_table = "TastingInformations"


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)