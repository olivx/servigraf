# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf.urls import url
from project import views as views_prject

urlpatterns = [

    url(r'projects_list/$' , views_prject.project_list, name='project_list'),
    url(r'projects_update/(?P<pk>\d+)/$', views_prject.project_update, name='project_update'),
    url(r'projects_detail/(?P<pk>\d+)/$', views_prject.project_detail, name='project_detail'),
    url(r'projects_deactivate/(?P<pk>\d+)/$', views_prject.project_deactivate, name='project_deactivate'),
    url(r'project_create/', views_prject.project_create, name="project_create"),
    url(r'projects_create/(?P<pk>\d+)/cliente/$', views_prject.project_client_create,
        name='project_create_client'),

    url(r'projects_autocomplete/client/$', views_prject.project_client_autocomplete,
        name='project_autocomplete_client'),
    url(r'projects_autocomplete/service/$', views_prject.project_service_autocomplete,
        name='project_autocomplete_service'),


]
