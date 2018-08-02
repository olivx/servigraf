from django.conf.urls import url
from client import views as client_views

urlpatterns = [
    url(r'ticket_list/$', client_views.ticket_list, name='ticket_list'),
]
