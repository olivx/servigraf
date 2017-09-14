from django.shortcuts import render, get_object_or_404

from project.models import Projects


def projeto_detail(request, pk):
    project = get_object_or_404(Projects, pk=pk)
    return render(request, 'project_details.html', {'project': project})
