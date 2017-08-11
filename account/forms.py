import re
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms import ValidationError
from django import forms


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')


class PasswordChange(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PasswordChange, self).__init__(*args, **kwargs)

    old_password = forms.CharField(max_length=35, min_length=8, widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(max_length=35, label='Password ', widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(max_length=35, label='Password Confirm', widget=forms.PasswordInput, required=True)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise ValidationError('O password não é o mesmo que o Antigo')

        return old_password

    def clean_new_password2(self):
        pass1 = self.cleaned_data['new_password1']
        pass2 = self.cleaned_data['new_password2']

        if pass1 != pass2:
            raise ValidationError('Passwords não são identicos ')

        if len(pass2) < 8:
            raise ValidationError('Passord precisa de pelo menos 8 caracteres')

        if not any(char.isdigit() for char in pass2):
            raise ValidationError('Password precisa conter um numero pelo menos ')

        if not any(char.isalpha() for char in pass2):
            raise ValidationError('Password precisa conter Letras e Numeros ')

        return pass2


class PasswordResetConfirm(forms.Form):
    new_password1 = forms.CharField(max_length=35, label='Password ', widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(max_length=35, label='Password Confirm', widget=forms.PasswordInput, required=True)

    def clean_new_password2(self):
        pass1 = self.cleaned_data['new_password1']
        pass2 = self.cleaned_data['new_password2']

        if pass1 != pass2:
            raise ValidationError('Passwords não são identicos ')

        if len(pass2) < 8:
            raise ValidationError('Passord precisa de pelo menos 8 caracteres')

        if not any(char.isdigit() for char in pass2):
            raise ValidationError('Password precisa conter um numero pelo menos ')

        if not any(char.isalpha() for char in pass2):
            raise ValidationError('Password precisa conter Letras e Numeros ')

        return self.cleaned_data


class EmailUsernameAuthenticationForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:
            try:
                username = User.objects.get(email=username)
            except ObjectDoesNotExist:
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return username
