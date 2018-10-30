from django import forms
from django.forms import ModelForm
from .models import *

class LocationsForm(ModelForm):
    class Meta:
        model = Locations
        labels = {
            "LocationName" : "Lokasyon Adı:"
        }
        fields = ['LocationName']

class MachinesForm(ModelForm):
    class Meta:
        model = Machines
        labels= {
            "Name" : "Makine Adı",
            "SerialNumber" : "Seri Numarası",
            "Fee" : "Fiyatı",
        }
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(MachinesForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PersonnelsForm(ModelForm):
    class Meta:
        model = Personnels
        labels= {
            "name" : "İsim",
            "surname" : "Soyisim",
            "LocationId" : "Lokasyon",
            "phone_number" : "Telefon Numarası"
        }
        exclude = ["location_id","user","birthday","wage"]
    #Aşağıdaki init constuctoru,ModelForm'un baz aldığı Model'daki fieldların hepsine
    #ortak olarak eklemek istediğimiz css class'ları kolayca eklemek için kullanıldı.
    #Aksi taktirde views.py içerisinden tüm fieldlara aynı css class'larını tek tek
    #eklememiz gerekecekti.
    def __init__(self, *args, **kwargs):
        super(PersonnelsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserForm(forms.Form):
    username = forms.CharField(label="Personel Kullanıcı Adı",max_length=200)
    password = forms.CharField(label="Personel Şifre",widget=forms.PasswordInput)
    email = forms.EmailField(label="Personel Email", max_length=255)
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AutoUserForm(ModelForm):
    class Meta:
        model=User
        labels = {
            "username" : "Personel Kullanıcı Adı",
            "password": "Personel Şifre",
            "email" : "Personel Email"
        }
        fields=("username","password","email",)
    def __init__(self, *args, **kwargs):
        super(AutoUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class StockForm(forms.Form):
    LocationName = forms.ModelChoiceField(queryset=Locations.objects.values_list('LocationName',flat=True))
    stock = forms.IntegerField()
    class Meta:
        labels = {
            "LocationName" : "Lokasyon Adı:",
            "stock": "Stok:"
        }
    def __init__(self, *args, **kwargs):
        super(StockForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'