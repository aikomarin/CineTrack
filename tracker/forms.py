from django import forms
from .models import SeriePelicula


class SeriePeliculaForm(forms.ModelForm):
    class Meta:
        model = SeriePelicula
        fields = [
            'titulo', 'tipo', 'plataforma', 'calificacion', 'veces_vista',
            'volveria_a_ver', 'estado', 'tendra_continuacion', 'favorita'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'plataforma': forms.Select(attrs={'class': 'form-control'}),
            'calificacion': forms.Select(attrs={'class': 'form-control'}),
            'veces_vista': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'volveria_a_ver': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'tendra_continuacion': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'favorita': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BuscarContenidoForm(forms.Form):
    query = forms.CharField(label='Buscar película o serie', max_length=100)
