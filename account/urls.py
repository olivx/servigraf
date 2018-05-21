from django.conf.urls import url
from account.forms import EmailUsernameAuthenticationForm
from account import views as account_views
from django.contrib.auth import views as auth_views
urlpatterns = [

    # login logout
    # url(r'login/$', auth_views.login,
    #     {
    #         'template_name': 'login.html',
    #         'authentication_form' : EmailUsernameAuthenticationForm
    #
    #     },  name='login'),
    url(r'login/$', account_views.login,  name='login'),
    url(r'logout', auth_views.logout ,{'next_page': '/'},  name='logout'),

    # reset password
    url(r'reset/passwod_reset/$', account_views.reset_password , name='reset_password'),
    url(r'reset/password_reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        account_views.password_confirm, name='password_confirm'),
    url(r'reset/password_reset/complete/$', account_views.password_reset_complete, name='reset_password_complete'),

    # change password
    url(r'change/change_password/', account_views.change_password, name='change_password')


]
