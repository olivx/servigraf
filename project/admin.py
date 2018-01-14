# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

# Register your models here.
from project.models import Projects, ProjectServices


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):
    list_filter = ['active']
    search_fields = ['name', 'desc']
    list_display = ['name' , 'user' , 'created' , 'updated']
    fields = ['name', 'desc', 'active' , 'user', 'created']

@admin.register(ProjectServices)
class ProjectServices(admin.ModelAdmin):
    pass
