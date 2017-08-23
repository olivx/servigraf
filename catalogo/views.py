from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.template.loader import render_to_string
from catalogo.models import Produto, GroupProduct
from core.utils import paginator
from django.shortcuts import get_object_or_404, resolve_url as r
from catalogo.forms import ProductForm, GroupProductForm
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
            prod = form.save()
            products = paginator(request, Produto.objects.all(), 5)
            message = 'Produto: {} Adicionado com sucesso! '.format(prod.nome.upper())
            messages.success(request, message)
            data['is_form_valid'] = True
            data['message'] = render_to_string('messages.html', {}, request=request)
            data['html_table'] = render_to_string('product_table.html', {'produto_list': products.object_list},
                                                  request=request)
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
        produto = get_object_or_404(Produto, pk=kwargs['pk'])
        form = ProductForm(request.POST, instance=produto)
        if form.is_valid():
            prod = form.save()
            message = 'Produto: {},  Alterado com sucesso!'.format(prod.nome.upper())
            messages.warning(request, message)
            products = paginator(request, Produto.objects.all(), 5)
            data['is_form_valid'] = True
            data['message'] = render_to_string('messages.html', {}, request=request)
            data['html_table'] = render_to_string('product_table.html',
                                                  {'produto_list': products.object_list}, request=request)
        else:
            data['is_form_valid'] = False
            data['html_form'] = \
                render_to_string('product_modal_update.html', {'form': form}, request=request)
        return JsonResponse(data)


product_update = ProductUpdate.as_view()


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Produto

    def get(self, request, *args, **kwargs):
        data = {}
        prod = get_object_or_404(Produto, pk=kwargs['pk'])
        form = ProductForm(instance=prod)
        data['html_form'] = \
            render_to_string('product_modal_delete.html', {'form': form}, request=request)
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        prod = get_object_or_404(Produto, pk=kwargs['pk'])
        prod.delete()
        message =  'Produto: {}, Deletado com suscesso!'.format(prod.nome.upper())
        messages.warning(request, message)
        return HttpResponseRedirect(r('catalogo:product_list'))

product_delete = ProductDelete.as_view()



class GroupProductList(LoginRequiredMixin, ListView):
    model = GroupProduct
    template_name = 'group_modal_crud.html'
    context_object_name = 'group_list'

    def get(self, request, *args, **kwargs):
        data = {}
        data['html_form'] = \
            render_to_string('group_modal_form.html', {'group_form': GroupProductForm()}, request=request)
        return JsonResponse(data)

group_list = GroupProductList.as_view()