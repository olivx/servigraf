from django.conf.urls import url
from core import views


urlpatterns = [
    url(r'clientes/$', views.clientes, name='clientes'),
    url(r'clientes/save/$', views.save_client, name='save_client'),
    url(r'clientes/update/(?P<pk>\d+)/$', views.update_client, name='update_client'),
    url(r'clientes/delete/(?P<pk>\d+)/$', views.delete_client, name='delete_client'),
    url(r'clientes/detalhes/(?P<pk>\d+)', views.detail_client, name='detail_client'),

    url('contatos/$', views.contact_list, name='contact_list'),
    url('contatos/save/$', views.contact_save, name='contact_save')

]
