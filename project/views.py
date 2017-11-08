from django.contrib import messages
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, ListView, CreateView
from django.shortcuts import render, redirect ,get_object_or_404, resolve_url as r

from project.forms import ProjectCreateClientForm
from project.models import Projects, ProjectServices

from core.models import Cliente
from catalogo.models import Produto


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Projects
    pk_url_kwarg = 'pk'

    def project_name(self):
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super(ProjectDetail, self).get_context_data(*args, **kwargs)
        context['project_client_list'] = self.object.clients.all()
        context['project_services_list'] = ProjectServices.objects.all()

        return context


projeto_detail = ProjectDetail.as_view()


class ProjectAutocompleteService(LoginRequiredMixin, ListView):
    model = Produto


class ProjectAutocomplieteClient(LoginRequiredMixin, ListView):
    model = Cliente

    def get(self, request, *args, **kwargs):
        term = request.GET.get('term')
        _list = []
        if term:
            client_list = Cliente.objects.filter(nome_fantasia__icontains=term)
            _list = [dict(id=client.pk, label=client.nome_fantasia, value=client.nome_fantasia) \
                     for client in client_list]

        return JsonResponse(_list, safe=False)


projeto_cliente_autocomplete = ProjectAutocomplieteClient.as_view()


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
        form = ProjectCreateClientForm(request.POST)
        project = get_object_or_404(Projects, pk=kwargs['pk'])

        if form.is_valid():
            print('é valido')
            print(form.cleaned_data['client'])
            import ipdb; ipdb.set_trace()

            client = get_object_or_404(Cliente, nome_fantasia__icontains=form.cleaned_data['client'])
            print('é o cliente  ',client)
            project.clients.add(client)
            project.save()
            messages.success(request, 'Cliente adicionado com sucesso!')
            data['is_form_valid'] = True
            data['html_form'] = render_to_string('project/project_form_create.html',
                                                 context={'form': form}, request=request)

        return redirect(r('projects:project_detail', pk=project.id))


projeto_cliente_create = ProjectCreateClients.as_view()


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Projects
