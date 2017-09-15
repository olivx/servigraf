from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from project.models import Projects


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Projects
    pk_url_kwarg = 'pk'


projeto_detail = ProjectDetail.as_view()
