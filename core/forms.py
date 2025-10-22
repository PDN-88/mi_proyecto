from django import forms
from .models import Inmueble

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ["tipo", "direccion", "planta", "puerta", "metros", "habitaciones", "propietario"]