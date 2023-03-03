from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
    
    imagen = forms.ImageField(required=True)
    texto = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Publicacion
        fields = ['titulo', 'imagen', 'texto']
        labels = {
            'titulo': 'Título',
        }
