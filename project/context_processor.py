from project.models import Projects


def project_list(request):
    return {
        'project_list': Projects.objects.all()
    }
