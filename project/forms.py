from django import forms

from project.models import Projects


class ProjectCreateClientForm(forms.ModelForm):

        class Meta:
            model = Projects
            fields = ('name', 'clients')