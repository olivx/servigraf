from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.template.loader import render_to_string
from catalogo.models import Produto
from core.utils import paginator
from django.shortcuts import get_object_or_404
from catalogo.forms import ProductForm
from pure_pagination.mixins import PaginationMixin


# Create your views here.

class ProductList(PaginationMixin, LoginRequiredMixin, ListView):
    model = Produto
    paginate_by = 5
    template_name = 'product_list.html'

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


product_list = ProductList.as_view()


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Produto

    def get(self, request, *args, **kwargs):
        data = {}
        form = ProductForm()
        data['html_form'] = \
            render_to_string('product_modal_save.html', {'form': form}, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            products = paginator(request, Produto.objects.all(), 5)
            data['message'] = 'Produto adicionado com sucesso! '
            data['is_form_valid'] = True
            data['html_table'] = \
                render_to_string('product_table.html', {'produto_list': products.object_list}, request=request)
        else:
            data['is_form_valid'] = False
            data['html_form'] = \
                render_to_string('product_modal_save.html', {'form': form}, request=request)
        return JsonResponse(data)


product_create = ProductCreate.as_view()


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Produto

    def get(self, request, *args, **kwargs):
        data = {}
        prod = get_object_or_404(Produto, pk=kwargs['pk'])
        form = ProductForm(instance=prod)
        data['html_form'] = \
            render_to_string('product_modal_update.html', {'form': form}, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        prod = get_object_or_404(Produto, pk=kwargs['pk'])
        form = ProductForm(request.POST, instance=prod)
        if form.is_valid():
            form.save()
            products = paginator(request, Produto.objects.all(), 5)
            data['message'] = 'Produto alterado com sucesso! '
            data['is_form_valid'] = True
            data['html_table'] = \
                render_to_string('product_table.html', {'produto_list': products.object_list}, request=request)
        else:
            data['is_form_valid'] = False
            data['html_form'] = \
                render_to_string('product_modal_update.html', {'form': form}, request=request)
        return JsonResponse(data)


product_update = ProductUpdate.as_view()
