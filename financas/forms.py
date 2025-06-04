from django import forms
from .models import Lucro, Despesa, Objetivo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LucroForm(forms.ModelForm):
    class Meta:
        model = Lucro
        fields = ['valor']

class DespesaForm(forms.ModelForm):
    class Meta:
        model = Despesa
        fields = ['valor']

class ObjetivoForm(forms.ModelForm):
    class Meta:
        model = Objetivo
        fields = ['nome', 'valor_meta']

class MovimentoObjetivoForm(forms.Form):
    valor = forms.DecimalField(label="Valor", max_digits=10, decimal_places=2)

class CadastroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

