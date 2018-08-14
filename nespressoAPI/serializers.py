from rest_framework import serializers
from .models import Sales,Machines,Personnels,Managers,Supervisors,Locations,TastingInformations,IntensiveHours,MachineConditions

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