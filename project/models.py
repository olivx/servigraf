from django.db import models
from django.shortcuts import resolve_url as r
# Create your models here.

class Projects(models.Model):

    name = models.CharField('Projeto', max_length=200)
    desc = models.TextField('Desccrição')

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('projects:project_detail', pk=self.pk)







