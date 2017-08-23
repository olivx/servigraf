from django.conf.urls import url
from catalogo import views as catalogo_views

urlpatterns = [

    url(r'product/list/$', catalogo_views.product_list, name='product_list'),
    url(r'product/create/$', catalogo_views.product_create, name='product_create'),
    url(r'product/update/(?P<pk>\d+)/$', catalogo_views.product_update, name='product_update'),

]