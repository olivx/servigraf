from django import forms
from django.core.exceptions import ValidationError

from catalogo.models import Produto


class ProductForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ('nome', 'desc', 'tipo', 'obs', 'valor',
                  'quantidade', 'ativo', 'grupo')

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade is None or quantidade < 0:
            quantidade = 0
        return quantidade

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor <= 0:
            raise ValidationError('Valor precisa ser maior que zero')
        return valor
