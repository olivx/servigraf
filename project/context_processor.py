# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from project.models import Projects


def project_list(request):
    return {
        'project_list': Projects.objects.filter(active=True)
    }
