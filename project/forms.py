from django import forms
from django.core.exceptions import ValidationError

from core.models import Cliente
from project.models import Projects


class ProjectCreateClientForm(forms.Form):
    client = forms.CharField(label='Cliente', max_length='255', required=True)
    project = forms.CharField(label='Projeto', max_length='255',
                              widget=forms.HiddenInput())

    def clean(self):
        project = self.cleaned_data.get('project')
        client = self.cleaned_data.get('client')
        # import ipdb; ipdb.set_trace()
        if not Cliente.objects.filter(nome_fantasia__icontains=client).exists():
            self.add_error('client', ValidationError('Cliente não encontrado '))
            return self.cleaned_data

        if Projects.objects.filter(name=project).first()\
                .clients.filter(nome_fantasia__icontains=client).exists():
            self.add_error('client', ValidationError('Cliente já cadastrado no projeto.'))
            return self.cleaned_data

        return self.cleaned_data

class ProjectCreateServiceForm(forms.Form):
    service = forms.CharField(label='Servico', max_length='255')
    price = forms.DecimalField(label='Preço', max_digits=6,decimal_places=2,required=True)
    project = forms.CharField(label='Projeto', max_length='255', required=True,  widget=forms.HiddenInput())


