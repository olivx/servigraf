from django.conf.urls import url
from django.contrib.auth import views as view_auth
from account.forms import EmailUsernameAuthenticationForm
urlpatterns = [

    url(r'login/$', view_auth.login,
        {
            'template_name': 'registration/login.html',
            'authentication_form' : EmailUsernameAuthenticationForm

        },  name='login'),
    url(r'logout', view_auth.logout ,{'next_page': '/'},  name='logout'),

]