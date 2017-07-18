from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger

# Create your views here.
from core.forms import ClientForm
from core.models import Cliente
from core.utils import paginator


def home(request):
    return render(request, 'index.html', {})


def clientes(request):
    template = 'clientes/client_list.html'
    search = request.GET.get('search')
    if search is not None:
        clients_list = Cliente.objects.filter(Q(ativo=True) &
                                              Q(nome_fantasia__contains=search,
                                                razao_social__icontains=search))
    else:
        clients_list = Cliente.objects.filter(ativo=True)
    return render(request, template, {'client_list': paginator(request=request,object_list=clients_list)})


def save_client(request):
    data = {}
    template = 'clientes/client_modal_save.html'
    template_success = 'clientes/client_table.html'
    if request.method == 'POST':
        form_client = ClientForm(request.POST)
        if form_client.is_valid():
            form_client.save()
            data['is_form_valid'] = True
            client_list = Cliente.objects.filter(ativo=True)
            context = {
                'client_list': paginator(request,client_list)
            }
            data['message'] = 'cliente: {} foi adicionado com sucesso!'.format(
                form_client.cleaned_data['nome_fantasia'])
            data['html_table'] = render_to_string(template_success, context=context, request=request)
        else:
            data['is_form_valid'] = False
            data['message'] = 'Erros foram processado durante a ação,\npor favor verifique o formulario e tente ' \
                              'novamente. '
            data['html_form'] = render_to_string(template,
                                                 {'form_client': form_client}, request=request)

    else:
        form_client = ClientForm()
        context = {
            'form_client': form_client
        }
        data['html_form'] = render_to_string(template, context, request=request)
    return JsonResponse(data)


def update_client(request, pk):
    data = {}
    template = 'clientes/client_modal_update.html'
    template_success = 'clientes/client_table.html'
    client = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form_client = ClientForm(request.POST, instance=client)
        if form_client.is_valid():
            form_client.save()
            client_list = Cliente.objects.filter(ativo=True)
            context = {
                'client_list': paginator(request, client_list)
            }
            data['is_form_valid'] = True
            data['message'] = 'cliente: {} foi Alterado com Sucesso!'\
                .format(form_client.cleaned_data['nome_fantasia'])

            data['html_table'] = render_to_string(template_success, context=context, request=request)
        else:
            data['is_form_valid'] = False
            data['message'] = 'Erros foram processado durante a ação,\npor favor verifique o formulario e tente ' \
                              'novamente. '
            data['html_form'] = render_to_string(template, {'form_client': form_client}, request=request)

    else:
        form_client = ClientForm(instance=client)
        data['html_form'] = render_to_string(template, {'form_client': form_client}, request=request)

    return JsonResponse(data)


def delete_client(request, pk):
    data = {}
    template = 'clientes/client_modal_delete.html'
    template_success = 'clientes/client_table.html'
    client = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        client.ativo = False
        client.save()
        data['is_form_valid'] = True
        data['message'] = 'Cliente: {0} \nDesativado com sucesso.\n\n' \
                          'para reativa-lo você precisa usar a area administrativa.' \
            .format(client)
        cliente_list = Cliente.objects.filter(ativo=True)
        data['html_table'] = render_to_string(template_success, {'client_list': paginator(request, cliente_list) },
                                              request=request)

    else:
        form_client = ClientForm(instance=client)
        data['html_form'] = render_to_string(template, {'form_client': form_client},
                                             request=request)
    return JsonResponse(data)


def detail_client(request, pk):
    tempate_name = 'clientes/client_detail.html'
    client = get_object_or_404(Cliente, pk=pk)
    form_client =  ClientForm(instance=client)
    context = {
        'form_client': form_client
    }
    return render(request, tempate_name, context)


def contact_list(request):
    return render(request, 'contact/contact_list.html')
