from django.conf.urls import url
from project import views as views_prject

urlpatterns = [

    url(r'projects_detail/(?P<pk>\d+)$', views_prject.projeto_detail, name='project_detail'),

]