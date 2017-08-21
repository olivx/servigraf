from django.views.generic import ListView
from catalogo.models import Produto
from catalogo.mixins import *
from pure_pagination.mixins import PaginationMixin
# Create your views here.


class ProdctList(SearchProductMixin, PaginationMixin, ListView):
    model = Produto
    paginate_by = 5
    template_name = 'product_list.html'
product_list = ProdctList.as_view()


