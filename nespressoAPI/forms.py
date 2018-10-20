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
            "phone_number" : "Telefon Numarası",
            "birthday" : "Doğum Günü"
        }
        exclude = ()
    #Aşağıdaki init constuctoru,ModelForm'un baz aldığı Model'daki fieldların hepsine
    #ortak olarak eklemek istediğimiz css class'ları kolayca eklemek için kullanıldı.
    #Aksi taktirde views.py içerisinden tüm fieldlara aynı css class'larını tek tek
    #eklememiz gerekecekti.
    def __init__(self, *args, **kwargs):
        super(PersonnelsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'