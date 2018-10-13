from django.forms import ModelForm
from .models import *

class LocationsForm(ModelForm):
    class Meta:
        model = Locations
        exclude = ()