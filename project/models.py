from django.db import models
from django.shortcuts import resolve_url as r


# Create your models here.

class Projects(models.Model):
    name = models.CharField('Projeto', max_length=200)
    desc = models.TextField('Desccrição')
    clients =  models.ManyToManyField('core.Cliente')
    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('projects:project_detail', pk=self.pk)



    class Meta:
        verbose_name = 'Projeto Cliente'
        verbose_name_plural = 'Projetos Clientes'


class ProjectServices(models.Model):
    project = models.ForeignKey('project.Projects')
    service = models.ForeignKey('catalogo.Produto', related_name='services')
    valor = models.DecimalField('Valor', decimal_places=2, max_digits=10)

    class Meta:
        verbose_name = 'Projeto Serviço'
        verbose_name_plural = 'Projetos Serviços'

    def __str__(self):
        return '%s | %s' % (self.service, self.valor)


class ProjetoSales(models.Model):
    client = models.ForeignKey('project.Projects')
    service = models.ForeignKey('project.ProjectServices')
    user = models.ForeignKey('auth.User')

    pi = models.CharField('PI', max_length=20)
    valor_unitario = models.DecimalField('Valor Unitario', decimal_places=2, max_digits=10)
    quantidade = models.PositiveIntegerField('Valor Unitario')
    acabamento = models.DecimalField('Acabamento', decimal_places=2, max_digits=10, null=True, blank=True)
    timestamp = models.DateField('Data pedido')
    entrega = models.TimeField('Horario de Entrega')
    obs = models.TextField('Observação', null=True, blank=True)
