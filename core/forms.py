import re
from django import forms
from core import utils
from django.core.exceptions import ValidationError
from core.models import Cliente, Contato, Email, Telefone, Endereco


class ClientForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('razao_social', 'nome_fantasia', 'documento',
                  'tipo', 'observacao', 'ramo', 'mensalista')

    def clean_razao_social(self):
        razao_social = self.cleaned_data.get('razao_social')

        if len(razao_social) < 3:
            raise ValidationError('Razão Social não pode ter menos que 3 Letras.', code='MIN_3')

        words = [w.upper() for w in razao_social.split()]
        return ' '.join(words)

    def clean_nome_fantasia(self):
        nome_fantasia = self.cleaned_data.get('nome_fantasia')
        if len(nome_fantasia) < 3:
            raise ValidationError('Nome Fantasia não pode ter menos de 3 letras.', code='MIN_3')
        return ''.join(n.upper() for n in nome_fantasia)

    def clean_documento(self):
        pattern = re.compile('\d+')
        documento = pattern.findall(self.cleaned_data.get('documento'))

        return ''.join(documento)

    def clean(self):
        documento = self.cleaned_data.get('documento')
        tipo = self.cleaned_data.get('tipo')
        # cnpj precisa ser informado.
        if not documento:
            if tipo == 1:
                self.add_error('documento','CNPJ precisa ser informado.')
                raise ValidationError('CNPJ precisa ser informado.', code='CNPJ_REQUIRED')
            else:
                self.add_error('documento', 'CPF precisa ser informado')
                raise ValidationError('CPF precisa ser informado', code='CPF_REQUIRED')

        # não pode validar um cpf se o tipo for cnpj
        if tipo == 1:
            if not utils.validar_cnpj(documento):
                self.add_error('documento','CNPJ informado invalido, verifique e tente novamente.')
                raise ValidationError('CNPJ informado invalido, verifique e tente novamente.', code='CNPJ_INVALIDO')

        elif tipo == 2:
            if not utils.validar_cpf(documento):
                self.add_error('documento','CPF informado invalido, verifique e tente novamente.')
                raise ValidationError('CPF informado invalido, verifique e tente novamente.', code='CPF_INVALIDO')

        return self.cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ('nome', 'sobre_nome', 'observacao',)


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('email',)


class TelefoneFrom(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = ('tipo', 'telefone',)


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ('cliente', 'cep', 'endereco', 'numero', 'complemento',
                  'bairro', 'cidade', 'uf', 'observacao', 'tipo_end')
