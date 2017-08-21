from catalogo.models import Produto
from django.db.models import Q


class SearchProductMixin(object):
    def get_queryset(self):
        products = Produto.objects.all()
        search = self.request.GET.get('search')
        if search is not None:
            try:
                _id = int(search)
                products = products.filter(id=_id)
            except ValueError:
                products = products.filter(Q(nome__contains=search) |
                                           Q(desc__contains=search)).order_by('nome')
        return products
