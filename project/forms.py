from django import forms

from project.models import Projects


class ProjectCreateClientForm(forms.Form):

        client =   forms.CharField(label='Cliente', max_length='255')
        project =  forms.CharField(label='Cliente', max_length='255')
