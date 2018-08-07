from django import forms
from client.models import CatalogoGrupo

class CatalogoGrupoForm(forms.ModelForm):

    class Meta:
        model = CatalogoGrupo
        fields = ('grupo', 'produto', 'valor',)
