from django.conf.urls import url
from core import views


urlpatterns = [
    url(r'clientes/$', views.clientes, name='clientes'),
    url(r'clientes/save/$', views.save_client, name='save_client'),
    url(r'clientes/update/(?P<pk>\d+)/$', views.update_client, name='update_client'),
    url(r'clientes/delete/(?P<pk>\d+)/$', views.delete_client, name='delete_client'),
    url(r'clientes/detalhes/(?P<pk>\d+)/$', views.detail_client, name='detail_client'),

    url(r'contatos/save/(?P<client_id>\d+)/$', views.contact_save, name='contact_save'),
    url(r'contatos/update/(?P<client_id>\d+)/(?P<contact_id>\d+)/$', views.contact_update, name='contact_update'),
    url(r'contatos/delete/(?P<client_id>\d+)/(?P<contact_id>\d+)/$', views.contact_delete, name='contact_delete'),

    url(r'endereco/save/(?P<client_id>\d+)/$', views.end_save, name='end_save')

]
