from django.db import models

class Managers(models.Model):
    Name = models.CharField(max_length=200)
    Surname = models.CharField(max_length=200)
    #Meta sınıfı olmadan modeli migrate ettigimizde django appname_tablename şeklinde isimlendiriyor. Bunun önüne geçmek için Meta sınıfıyla tabloya isim veriyoruz.
    class Meta:
        db_table = "Managers"


class Locations(models.Model):
    Latitude = models.FloatField()
    Longtitude = models.FloatField()
    LocationName = models.CharField(max_length=1000)
    class Meta:
        db_table = "Locations"

class Personnels(models.Model):
    LocationId = models.ForeignKey(Locations,on_delete=models.CASCADE,db_column='LocationId')
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
    Location = models.ForeignKey(Locations,on_delete=models.CASCADE)
    IsActive = models.BooleanField()
    class Meta:
        db_table = "Supervisors"
    
class Sales(models.Model):
    MachineId = models.ForeignKey(Machines,on_delete=models.CASCADE,db_column='MachineId')
    PersonnelId = models.ForeignKey(Personnels,on_delete=models.CASCADE,db_column='PersonnelId')
    #SerialNumber = models.CharField(max_length=1000) #Seri numarası tekrar eklemek gerekli mi düşün.
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
    PersonnelId = models.ForeignKey(Personnels,on_delete=models.CASCADE,db_column='PersonnelId')
    MachineConditionId = models.ForeignKey(MachineConditions,on_delete=models.CASCADE,db_column='MachineConditionId')
    IntensiveHoursId = models.ForeignKey(IntensiveHours,on_delete=models.CASCADE,db_column='IntensiveHoursId')

    TotalEspressoRecipe = models.IntegerField() #Yapılan toplam espresso tarif
    TotalMilkyRecipe = models.IntegerField() #Yapılan toplam sütlü tarif
    DailyCoffeeComsumption = models.IntegerField() #Günlük tüketilen kahve adedi
    DailyShopCoffeeConsumption = models.IntegerField() #Günlük mağazanın kullandığı kahve adeti
    DailyMilkBoxConsumption = models.IntegerField() #Günlük kullanılan süt (kutu)
    class Meta:
        db_table = "TastingInformations"