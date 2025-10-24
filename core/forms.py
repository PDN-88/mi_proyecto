from django import forms
from .models import Inmueble, Incidencia

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ["tipo", "direccion", "planta", "puerta", "metros", "habitaciones", "propietario"]

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ['inmueble', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and not user.is_staff:
            # For tenants, limit the property choices to those they are associated with
            self.fields['inmueble'].queryset = Inmueble.objects.filter(
                contratos__inquilinos__usuario=user
            ).distinct()
