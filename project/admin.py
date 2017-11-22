from django.contrib import admin

# Register your models here.
from project.models import Projects, ProjectServices


@admin.register(Projects)
class ProjectsAdmin(admin.ModelAdmin):

    search_fields = ['name', 'desc']
    fields = ['name', 'desc']


@admin.register(ProjectServices)
class ProjectServices(admin.ModelAdmin):
    pass
