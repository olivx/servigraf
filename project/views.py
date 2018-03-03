# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.shortcuts import render, redirect, get_object_or_404, resolve_url as r

from project.forms import ProjectCreateClientForm, ProjectCreateServiceForm
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

    def get(self, request, *args, **kwargs):
        pass
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = request.POST.get('title')
        desc = request.POST.get('descricao')
        project = request.POST.get('id_project')

        if title:
            _project = Projects.objects.filter(name__iexact=title)
            if _project.first():
                if not _project.first().active:
                    messages.warning(request, ' Projeto: {},\
                        já existe na lista de projetos, mas se encontra com o estatus inativo.\
                        para ativa-lo é necessario fazer login na administrativa.'
                            .format(title.upper()))
                
                else:
                    messages.warning(request, ' Projeto: {}, já existe na lista de projetos.'
                            .format(title.upper()))
                    
                return redirect('projects:project_list')
                
            project = Projects.objects.get(id=project)
            project.name = title
            project.desc = desc
            project.user = request.user
            project.save()
            
            messages.success(request, ' Projeto: {}, ALterado com sucesso.'.format(title))
        else:
            messages.warning(request, 'Título e Descrição são campo obrigatórios.')
       
        return redirect('projects:project_list')
project_update  = ProjectUpdate.as_view()        


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
        
        context['project_client_list'] = self.object.clients.all().order_by('nome_fantasia')
        context['project_services_list'] = ProjectServices.objects.filter(project= self.object).order_by('service__nome')

        return context
project_detail = ProjectDetail.as_view()


class ProjectAutocompleteService(LoginRequiredMixin, ListView):
    model = Produto

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        _list = []
        if term:
            service_list = Produto.objects.filter(tipo=2, nome__icontains=term)[:10]
            _list =  [dict(id=service.id, value=service.nome.upper(), 
                                label=service.nome.upper(), price=service.valor) 
                                    for service in service_list]
        
        return JsonResponse(_list, safe=False)
project_service_autocomplete = ProjectAutocompleteService.as_view()

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
            client_list = Cliente.objects.filter(nome_fantasia__icontains=term)[:10]
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
        data['html_form'] = render_to_string(self.template_name,
                                             context=context, request=request)

        return JsonResponse(data)

    def post(self, request, *args, **kwargs):

        # import ipdb; ipdb.set_trace()


        data = {}
        project = get_object_or_404(Projects, pk=kwargs['pk'])
        form = ProjectCreateClientForm(request.POST)
        client_id = request.POST.get('id_client')

        if form.is_valid():

            if client_id:
                client = get_object_or_404(Cliente, pk=client_id)

                ProjectClient.objects.create(project=project, clients=client)
                messages.success(request, 'Cliente adicionado com sucesso!')

                data['is_form_valid'] = True
                data['list_client'] = render_to_string('project/_list_client_project.html',
                                                   {'project_client_list': project.clients.all()}, 
                                                   request=request)

                context = {'project': project, 'form': form}
                data['html_form'] = render_to_string('project/project_form_create.html',
                                                   context=context, request=request)
            else:
                messages.warning(request, 'Cliente não encontrado.')                
            
            data['message'] = render_to_string('messages.html', {}, request=request)
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


class ProjectCreateService(LoginRequiredMixin, CreateView):
    template_name = 'project/project_service_form.html'
    model = ProjectServices
    form_class = ProjectCreateServiceForm

    def get(self, request, *args, **kwargs):
        data  = {}
        project = get_object_or_404(Projects, pk=kwargs['pk'])
        form_class =  self.get_form_class()
        form = self.get_form(form_class)
        context = {'project': project, 'form': form }
        data['html_form'] = render_to_string(self.template_name, 
                                context=context, request=self.request)
        return JsonResponse(data)       

    def post(self, request, *args, **kwargs):
        data  = {}
    
        # import ipdb; ipdb.set_trace()

        form =  ProjectCreateServiceForm(request.POST)
        if form.is_valid():
            _project = form.cleaned_data['project']
            _service = form.cleaned_data['service']
            _price = form.cleaned_data['valor']

            project = get_object_or_404(Projects, pk=_project)
            service = get_object_or_404(Produto, pk=_service)

            ProjectServices.objects.create(
                project=project, service=service, valor=_price)

            list_service = ProjectServices.objects.filter(project= project)
            context = {'project_services_list': list_service }
            
            data['service_list'] = render_to_string('project/_list_service_project.html', 
                context=context, request=request)

            messages.success(request, 'Servico adiconado com sucesso!')    
            data['is_form_valid'] = True 
        
        else:
            _project = form.cleaned_data['project']
            project = get_object_or_404(Projects, pk=_project)
            data['is_form_valid'] = False 
            context = {'project': project, 'form': form}
            data['html_form'] = render_to_string(self.template_name,
                                                 context=context, request=self.request)

            for key, value in form.errors.items():
                messages.error(request, value)

        data['message'] = render_to_string('messages.html', {}, request=request)
        return JsonResponse(data)
procject_create_service = ProjectCreateService.as_view()


class ProjectDeleteService(LoginRequiredMixin, DetailView):
    model = ProjectServices

    def post(self, request, *args, **kwargs):
        project_id = request.POST.get('project')
        service_id = request.POST.get('service')
        project_service = ProjectServices.objects.get(project__pk=project_id, service__pk=service_id)

        # logica para deletar somente se não houver venda lançada.
        # implementar

        project_service.delete()
        messages.success(request, 'Serviço removido com sucesso.')

        return redirect('projects:project_detail', pk=project_service.project.pk)
project_delete_service = ProjectDeleteService.as_view()

