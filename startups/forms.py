from django import forms
from .models import Startup

class StartupForm(forms.ModelForm):
    class Meta:
        model = Startup
        fields = [
            'nome',
            'cnpj',
            'representante',
            'email',
            'telefone',
            'fase',
            'modelo_incubacao',
            'plano',
            'ativo',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'representante': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'fase': forms.Select(attrs={'class': 'form-control'}),
            'modelo_incubacao': forms.Select(attrs={'class': 'form-control'}),
            'plano': forms.Select(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }