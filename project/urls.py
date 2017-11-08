from django.conf.urls import url
from project import views as views_prject

urlpatterns = [

    url(r'projects_detail/(?P<pk>\d+)/$', views_prject.projeto_detail, name='project_detail'),
    url(r'projects_create/(?P<pk>\d+)/$', views_prject.projeto_cliente_create,
        name='project_create'),

    url(r'projects_autocomplete/client/$', views_prject.projeto_cliente_autocomplete,
        name='project_autocomplete_client'),

]
