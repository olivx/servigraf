from django.conf.urls import url
from catalogo import views as catalogo_views

urlpatterns = [

    url(r'product/list/$', catalogo_views.product_list, name='product_list'),
    url(r'product/create/$', catalogo_views.prodcut_create, name='product_create'),

]