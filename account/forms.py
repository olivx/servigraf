import re
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms import ValidationError
from django import forms


class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='E-mail')

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
            raise ValidationError('Password precisa conter alpha numericos ')

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
