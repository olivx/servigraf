from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

# Create your views here.
from core.forms import ClientForm
from core.models import Cliente


def home(request):
    return render(request, 'index.html', {})


def clientes(request):
    template = 'clientes/client_list.html'
    from core.models import Cliente
    clients = Cliente.objects.filter(ativo=True)

    return render(request, template, {'client_list': clients})


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
                'client_list': client_list
            }
            data['message'] = 'cliente: {} foi Adicionado com Sucesso!'.format(
                form_client.cleaned_data['nome_fantasia'])
            data['html_table'] = render_to_string(template_success, context=context, request=request)
        else:
            data['is_form_valid'] = False
            data[
                'message'] = 'Erros foram processado durante a ação,\npor favor verifique o formulario e tente ' \
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
                'client_list': client_list
            }
            data['is_form_valid'] = True
            data['message'] = 'cliente: {} foi Alterado com Sucesso!'.format(form_client.cleaned_data['nome_fantasia'])
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
        client_ = client.save()
        data['is_form_valid'] = True
        data['message'] = 'Cliente: {0} \nDesativado com sucesso.\n\n' \
                          'para reativa-lo você precisa usar a area administrativa.' \
            .format(client)
        cliente_list = Cliente.objects.filter(ativo=True)
        data['html_table'] = render_to_string(template_success, {'client_list': cliente_list},
                                              request=request)

    else:
        form_client = ClientForm(instance=client)
        data['html_form'] = render_to_string(template, {'form_client': form_client},
                                             request=request)
    return JsonResponse(data)
