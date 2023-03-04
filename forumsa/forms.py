from .models import Publicacion
from django.contrib.auth.forms import UserCreationForm 
from .models import User
from django import forms

class PublicacionForm(forms.ModelForm):
    
    imagen = forms.ImageField(required=True)
    texto = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Publicacion
        fields = ['titulo', 'imagen', 'texto']
        labels = {
            'titulo': 'Título',
        }

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
            
        self.fields['email'].widget.attrs['class'] = 'w-full p-3 rounded dark:bg-gray-800'
        self.fields['username'].widget.attrs['class'] = 'w-full p-3 rounded dark:bg-gray-800'
        self.fields['password1'].widget.attrs['class'] = 'w-full p-3 rounded dark:bg-gray-800'
        self.fields['password2'].widget.attrs['class'] = 'w-full p-3 rounded dark:bg-gray-800'
            
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat Password'
        