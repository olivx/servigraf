from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

# Create your views here.
from core.forms import ClientForm, ContactForm, EmailForm, TelefoneFrom, EnderecoForm
from django.forms import inlineformset_factory
from core.models import Cliente, Contato, Email, Telefone, Endereco
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
    _contact_list = paginator(request, client.contatos.ativos(), 2)
    _end_list = paginator(request, client.enderecos.ativos(), 2)
    context = {
        'form_client': form_client,
        'contact_list': _contact_list,
        'end_list': _end_list
    }
    return render(request, tempate_name, context)


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
            contato = contact_form.save(commit=False)
            contato.cliente = client
            contato.save()
            email_formset.save()
            telefone_formset.save()
            _contact_list = paginator(request, client.contatos.ativos(), 2)
            data['is_form_valid'] = True

            data['message'] = 'Contado: {} do cliente {},\nadicionado com sucesso.'. \
                format(contato.nome.upper(), client.nome_fantasia.upper())

            data['html_table'] = render_to_string('contact/contact_table.html',
                                                  {
                                                      'form_client': form_client,
                                                      'contact_list': _contact_list
                                                  },
                                                  request=request)

            data['html_form'] = render_to_string('clientes/client_form.html',
                                                 {'form_client': form_client},
                                                 request=request)
        else:  # post not valid
            context = {
                'form_client': form_client,
                'form_contact': contact_form,
                'formset_email': email_formset,
                'formset_telefone': telefone_formset
            }

            data['is_form_valid'] = False
            data['html_form'] = render_to_string('contact/contact_save.html', context, request=request)
    else:  # if is a get
        context = {
            'form_client': form_client,
            'form_contact': contact_form,
            'formset_email': email_formset,
            'formset_telefone': telefone_formset

        }
        data['is_form_valid'] = True
        data['html_form'] = render_to_string('contact/contact_save.html', context, request=request)

    # return json
    return JsonResponse(data)


def contact_update(request, client_id, contact_id):
    data = {}
    # get client end contact instances
    client = get_object_or_404(Cliente, pk=client_id)
    contact = get_object_or_404(Contato, pk=contact_id)

    # formset
    email_contact_formset = inlineformset_factory(Contato, Email, form=EmailForm, can_delete=True,
                                                  min_num=0, extra=1, validate_min=True)

    telefone_contact_formset = inlineformset_factory(Contato, Telefone, form=TelefoneFrom, can_delete=True,
                                                     min_num=0, extra=1, validate_min=True)

    # forms initialization
    form_contact = ContactForm(request.POST or None, instance=contact, prefix='contact')
    email_formset = email_contact_formset(request.POST or None, instance=contact, prefix='email')
    telefone_formset = telefone_contact_formset(request.POST or None, instance=contact, prefix='telefone')
    form_client = ClientForm(instance=client)
    if request.method == 'POST':

        if form_contact.is_valid() and email_formset.is_valid() and telefone_formset.is_valid():
            forms = form_contact.save(commit=False)
            forms.cliente = client
            forms.save()
            email_formset.save()
            telefone_formset.save()

            _contact_list = paginator(request, client.contatos.ativos(), 2)
            context = {
                'contact_list': _contact_list,
                'form_client': form_client
            }
            data['is_form_valid'] = True
            data['message'] = 'Contato: {} do Cliente: {} ,\n alterado com sucesso.' \
                .format(contact.nome.upper() + contact.sobre_nome.upper(), client.nome_fantasia.upper())

            data['html_table'] = render_to_string('contact/contact_table.html', context, request=request)
            data['html_form'] = render_to_string('clientes/client_form.html', {'form_client': form_client},
                                                 request=request)


        else:  # post not valid
            context = {
                'form_client': form_client,
                'form_contact': form_contact,
                'formset_email': email_formset,
                'formset_telefone': telefone_formset
            }

            data['is_form_valid'] = False
            data['html_form'] = render_to_string('contact/contact_update.html', context, request=request)


    else:  # if is get
        context = {
            'form_client': form_client,
            'form_contact': form_contact,
            'formset_email': email_formset,
            'formset_telefone': telefone_formset
        }
        data['html_form'] = render_to_string('contact/contact_update.html', context, request=request)

    return JsonResponse(data)


def contact_delete(request, client_id, contact_id):
    data = {}
    client = get_object_or_404(Cliente, pk=client_id)
    contact = get_object_or_404(Contato, pk=contact_id)

    if request.method == 'POST':
        contact.ativo = False
        contact.save()
        _contact_list = paginator(request, client.contatos.ativos(), 2)
        form_client = ClientForm(instance=client)
        context = {
            'form_client': form_client,
            'contact_list': _contact_list,
        }
        data['message'] = 'Contato {} , desativado com sucesso.\n' \
                          'para ativalo é Necessario usar a area admistrativa'.format(contact)
        data['html_table'] = render_to_string('contact/contact_table.html', context, request=request)

    else:
        context = {
            'contact': contact,
            'client': client
        }
        data['html_form'] = render_to_string('contact/contact_delete.html', context, request=request)

    return JsonResponse(data)


def end_service(request, client_id , end , template_success):
    data = {}
    client = get_object_or_404(Cliente, pk=client_id)
    end.cliente = client
    if request.method == 'POST':
        pass
    else:
        data['disable_all'] = False
        end_form = EnderecoForm(instance=end)
        data['html_form'] = render_to_string(template_success,
                                             context={'end_form': end_form}, request=request)

    return JsonResponse(data)


def end_save(request, client_id):
    end = Endereco()
    return end_service(request, client_id, end, 'end/end_save.html')


def end_update(request, client_id, end_id):
    end = get_object_or_404(Endereco, pk=end_id)
    return end_service(request, client_id, end, 'end/end_update.html')


def end_delete(request, client_id, end_id):
    data = {}
    client = get_object_or_404(Cliente, pk=client_id)
    end = get_object_or_404(Endereco, pk=end_id)
    end.cliente = client

    if request.method == 'POST':
        pass

    else:
        end_form = EnderecoForm(instance=end)
        data['disable_all'] = True
        data['html_form'] = render_to_string('end/end_delete.html',
                                             context={'end_form': end_form}, request=request)


    return JsonResponse(data)



