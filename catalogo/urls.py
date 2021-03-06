from django.conf.urls import url
from catalogo import views as catalogo_views

urlpatterns = [

    url(r'product/list/$', catalogo_views.product_list, name='product_list'),
    url(r'product/create/$', catalogo_views.product_create, name='product_create'),
    url(r'product/update/(?P<pk>\d+)/$', catalogo_views.product_update, name='product_update'),
    url(r'product/delete/(?P<pk>\d+)/$', catalogo_views.product_delete, name='product_delete'),

    url(r'api/product/group/list/$', catalogo_views.group_list, name='group_list'),
    url(r'product/group/create/$', catalogo_views.group_create, name='group_create'),
    url(r'product/group/update/(?P<pk>\w+)$', catalogo_views.group_update, name='group_update'),
    url(r'product/group/delete/(?P<pk>\w+)$', catalogo_views.group_delete, name='group_delete'),

]