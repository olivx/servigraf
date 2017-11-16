from django import forms
from django.core.exceptions import ValidationError

from core.models import Cliente
from project.models import Projects


class ProjectCreateClientForm(forms.Form):
    client = forms.CharField(label='Cliente', max_length='255')
    project = forms.CharField(label='Projeto', max_length='255',
                              widget=forms.HiddenInput())

    def clean(self):
        project = self.cleaned_data.get('project')
        client = self.cleaned_data.get('client')

        if not Cliente.objects.filter(nome_fantasia__icontains=client).exists():
            self.add_error('client', ValidationError('Cliente não encontrado '))

        if Projects.objects.filter(clients=Cliente.objects.filter(nome_fantasia=client).first(),
                                   name=project).exists():
            self.add_error('client', ValidationError('Cliente já cadastrado no projeto.'))

        return self.cleaned_data
