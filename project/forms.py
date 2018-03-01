from django import forms
from django.core.exceptions import ValidationError

from core.models import Cliente
from catalogo.models import Produto
from project.models import Projects, ProjectServices


class ProjectCreateClientForm(forms.Form):
    client = forms.CharField(label='Cliente', max_length='255', required=True)
    project = forms.CharField(label='Projeto', max_length='255',
                              widget=forms.HiddenInput())

    def clean(self):
        project = self.cleaned_data.get('project')
        client = self.cleaned_data.get('client')
        if not Cliente.objects.filter(nome_fantasia__icontains=client).exists():
            self.add_error('client', ValidationError('Cliente não encontrado '))
            return self.cleaned_data

        if Projects.objects.filter(name=project).first()\
                .clients.filter(nome_fantasia__icontains=client).exists():
            self.add_error('client', ValidationError('Cliente já cadastrado no projeto.'))
            return self.cleaned_data

        return self.cleaned_data

class ProjectCreateServiceForm(forms.Form):
    
    service = forms.IntegerField(label='Servico', required=True,  widget=forms.HiddenInput())
    project = forms.IntegerField(label='Projeto', required=True,  widget=forms.HiddenInput())
    valor = forms.DecimalField(label='Preço', decimal_places=2, max_digits=10, required=True)

    def clean(self):
        project =  self.cleaned_data.get('project')
        service =  self.cleaned_data.get('service')

        if not Produto.objects.filter(pk=service).exists():
           self.add_error('service', ValidationError('Produto não encontrado no catalogo.'))
           return self.cleaned_data

        if ProjectServices.objects.filter(service__pk=service, project__pk=project).exists():
            self.add_error('service', ValidationError('Servico já existe no projeto'))
            return self.cleaned_data

        return self.cleaned_data
