from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.forms import ValidationError


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
                    params={'username': self.username_field.verbose_name },
                )
        return username