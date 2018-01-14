# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404, resolve_url as r

from project.forms import ProjectCreateClientForm
from project.models import Projects, ProjectServices, ProjectClient

from core.models import Cliente
from catalogo.models import Produto



class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Projects
    template_name = 'project/project_list.html'

    def post(self, request, *args, **kwargs):

        
        title = request.POST.get('title')
        desc = request.POST.get('descricao')
        
        if title:
            _project = Projects.objects.filter(name__iexact=title)
            if _project.first():
                if not _project.first().active:
                    messages.warning(request, ' Projeto: {}, \
                        já existe na lista de projetos, mas se encontra com o estatus inativo.\
                        para acessar é necessario fazer login na administrativa.'
                            .format(title.upper()))
                else:
                    messages.warning(request, ' Projeto: {}, já existe na lista de projetos.'
                            .format(title.upper()))
                    
                return redirect('projects:project_list')
                
            Projects.objects.create(name=title, desc=desc, user=request.user)
            messages.success(request, ' Projeto: {}, criado com sucesso.'.format(title))
            return redirect('projects:project_list')

        messages.warning(request, 'Título e Descrição são campo obrigatórios.')
        return redirect('projects:project_list')
project_create = ProjectCreate.as_view()


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Projects


class ProjectDeactivate(LoginRequiredMixin, UpdateView):
    model = Projects
    pk_url_kwarg = 'pk'
    template_name = 'project/project_list.html'


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.active = False
        self.object.save()

        messages.warning(request, 'Projecto: {}, foi desativardo. para reativa-lo use área administrativa.'
                                    .format(self.object.name))
        
        return redirect('projects:project_list')

project_deactivate =  ProjectDeactivate.as_view()

class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Projects
    pk_url_kwarg = 'pk'

    def project_name(self):
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetail, self).get_context_data(*args, **kwargs)
        context['project'] = self.object
        context['project_client_list'] = self.object.clients.all()
        context['project_services_list'] = ProjectServices.objects.all()

        return context
project_detail = ProjectDetail.as_view()


class ProjectAutocompleteService(LoginRequiredMixin, ListView):
    model = Produto


class ProjetoList(LoginRequiredMixin, ListView):
    model = Projects
    template_name = 'project/project_list.html'


    def get_queryset(self):
        return self.model.objects.filter(active=True)
project_list = ProjetoList.as_view()


class ProjectAutocomplieteClient(LoginRequiredMixin, ListView):
    model = Cliente

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        _list = []
        if term:
            client_list = Cliente.objects.filter(nome_fantasia__icontains=term)
            _list = [dict(id=client.pk, label=client.nome_fantasia, value=client.nome_fantasia)
                     for client in client_list]

        return JsonResponse(_list, safe=False)
project_client_autocomplete = ProjectAutocomplieteClient.as_view()


class ProjectCreateClients(LoginRequiredMixin, CreateView):
    model = Projects
    pk_url_kwarg = 'pk'
    template_name = 'project/project_company_save.html'
    form_class = ProjectCreateClientForm

    def get(self, request, *args, **kwargs):
        data = {}
        project = get_object_or_404(Projects, pk=kwargs['pk'])
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = {'project': project, 'form': form}
        data['html_form'] = render_to_string('project/project_form_create.html',
                                             context=context, request=request)

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = {}
        project = get_object_or_404(Projects, pk=kwargs['pk'])
        form = ProjectCreateClientForm(request.POST)

        if form.is_valid():
            client = get_object_or_404(
                Cliente, nome_fantasia__icontains=form.cleaned_data['client'])

            ProjectClient.objects.create(project=project, clients=client)
            messages.success(request, 'Cliente adicionado com sucesso!')

            data['is_form_valid'] = True
            data['message'] = render_to_string(
                'messages.html', {}, request=request)

            data['list_client'] = render_to_string('project/_list_client_project.html',
                                                   {'project_client_list': project.clients.all()}, request=request)

            context = {'project': project, 'form': form}
            data['html_form'] = render_to_string('project/project_form_create.html',
                                                 context=context, request=request)
            return JsonResponse(data)
        else:
            data['is_form_valid'] = False
            context = {'project': project, 'form': form}
            messages.error(request, 'Erro ao adicionar cliente !')
            data['message'] = render_to_string(
                'messages.html', {}, request=request)
            data['html_form'] = render_to_string('project/project_form_create.html',
                                                 context=context, request=request)

        return JsonResponse(data)
project_client_create = ProjectCreateClients.as_view()


