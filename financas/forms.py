from django import forms
from django.contrib.auth.models import User

class LucroForm(forms.Form):
    valor = forms.DecimalField(label="Valor", max_digits=10, decimal_places=2)

class DespesaForm(forms.Form):
    valor = forms.DecimalField(label="Valor", max_digits=10, decimal_places=2)

class ObjetivoForm(forms.Form):
    nome = forms.CharField(label="Nome", max_length=100)
    valor_meta = forms.DecimalField(label="Valor Meta", max_digits=10, decimal_places=2)

class MovimentoObjetivoForm(forms.Form):
    valor = forms.DecimalField(label="Valor", max_digits=10, decimal_places=2)

class CadastroForm(forms.Form):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

