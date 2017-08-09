from django.conf.urls import url
from django.contrib.auth import views as view_auth

urlpatterns = [

    url(r'login/$', view_auth.login,{'template_name': 'registration/login.html'},  name='login'),
    url(r'logout', view_auth.logout ,{'next_page': '/' },  name='logout'),

]