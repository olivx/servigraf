from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

# Create your views here.
from core.forms import ClientForm, ContactForm, EmailForm, TelefoneFrom
from django.forms import inlineformset_factory
from core.models import Cliente, Contato, Email, Telefone
from core.utils import paginator
from django.shortcuts import resolve_url as r


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

    clients = paginator(request, clients_list)
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
                'client_list': paginator(request, client_list)
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
            data['message'] = 'cliente: {} foi Alterado com Sucesso!' \
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
        data['html_table'] = render_to_string(template_success, {'client_list': paginator(request, cliente_list)},
                                              request=request)

    else:
        form_client = ClientForm(instance=client)
        data['html_form'] = render_to_string(template, {'form_client': form_client},
                                             request=request)
    return JsonResponse(data)


def detail_client(request, pk):
    tempate_name = 'clientes/client_detail.html'
    client = get_object_or_404(Cliente, pk=pk)
    form_client = ClientForm(instance=client)
    contatos = client.contatos.all()
    context = {
        'form_client': form_client,
        'contatos': contatos
    }
    return render(request, tempate_name, context)


def contact_list(request):
    return render(request, 'contact/contact_list.html')


def contact_save(request, client_id):
    data = {}
    contact = Contato()
    client = get_object_or_404(Cliente, pk=client_id)

    email_contact_formset = inlineformset_factory(Contato, Email, form=EmailForm,
                                                  can_delete=False,
                                                  extra=1, min_num=0, validate_min=True)
    telefone_contact_formset = inlineformset_factory(Contato, Telefone, form=TelefoneFrom,
                                                     can_delete=False,
                                                     extra=1, min_num=0, validate_min=True)

    contact_form = ContactForm(request.POST or None, instance=contact, prefix='contact')
    email_formset = email_contact_formset(request.POST or None, instance=contact, prefix='email')
    telefone_formset = telefone_contact_formset(request.POST or None, instance=contact, prefix='telefone')
    form_client = ClientForm(instance=client)
    if request.method == 'POST':
        if contact_form.is_valid() and email_formset.is_valid() and telefone_formset.is_valid():
            forms = contact_form.save(commit=False)
            forms.cliente = client
            forms.save()
            email_formset.save()
            telefone_formset.save()

            context = {
                'form_client': form_client,
                'contatos': client.contatos.all()
            }
            data['is_form_valid'] = True
            data['html_form'] = render_to_string('clientes/client_detail.html',
                                                 context, request=request)
        else:
            context = {
                'form_client': form_client,
                'form_contact': contact_form,
                'formset_email': email_formset,
                'formset_telefone': telefone_formset
            }

            data['is_form_valid'] = False
            data['html_form'] = render_to_string('contact/contact_save.html', context, request=request)
    else:
        context = {
            'form_client': form_client,
            'form_contact': contact_form,
            'formset_email': email_formset,
            'formset_telefone': telefone_formset

        }
        data['is_form_valid'] = True
        data['html_form'] = render_to_string('contact/contact_save.html', context, request=request)

    return JsonResponse(data)


def contact_update(request, client_id, contact_id):
    data = {}
    # get client end contact instances
    client = get_object_or_404(Cliente, pk=client_id)
    contact = get_object_or_404(Contato, pk=contact_id)

    # formset
    email_contact_formset = inlineformset_factory(Contato, Email, form=EmailForm, can_delete=False,
                                                  min_num=0, extra=1, validate_min=True)

    telefone_contact_formset = inlineformset_factory(Contato, Telefone, form=TelefoneFrom, can_delete=False,
                                                     min_num=0, extra=1, validate_min=True)

    # forms initialization
    contact_form = ContactForm(request.POST or None, instance=contact, prefix='contact')
    email_formset = email_contact_formset(request.POST or None, instance=contact, prefix='email')
    telefone_formset = telefone_contact_formset(request.POST or None, instance=contact, prefix='telefone')
    client_form = ClientForm(instance=client)
    if request.method == 'POST':

        if contact_form.is_valid() and email_formset.is_valid() and telefone_formset.is_valid():
            forms = contact_form.save(commit=False)
            forms.cliente = client
            forms.save()
            email_formset.save()
            telefone_formset.save()

            HttpResponseRedirect(r('servigraf:detail_client', pk=client_id))
    else:
        context = {
            'form_client': client_form,
            'form_contact': contact_form,
            'formset_email': email_formset,
            'formset_telefone': telefone_formset
        }
        data['html_form'] = render_to_string('contact/contact_update.html', context, request=request)

    return JsonResponse(data)
