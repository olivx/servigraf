from django.conf.urls import url
from catalogo import views as catalogo_views

urlpatterns = [

    url(r'produto/list/$', catalogo_views.product_list, name='product_list'),
]