from django.db import models


# Create your models here.


class Produto(models.Model):
    PRODUTO = 1
    SERVICO = 2
    TIPO_LIST = [
        (PRODUTO, 'produto'),
        (SERVICO, 'serviço')
    ]

    group = models.ForeignKey('catalogo.GroupProduct', null=True, blank=True, related_name='groups')

    nome = models.CharField('Nome', max_length=100)
    desc = models.TextField('Descrição', blank=True, null=True)
    tipo = models.PositiveIntegerField('Tipo', default=PRODUTO , choices=TIPO_LIST)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=2)
    obs = models.TextField('Observação', null=True, blank=True)
    quantidade = models.IntegerField('Quantidade', default=0, null=True, blank=True)
    data_create = models.DateTimeField('Criado', auto_now_add=True, auto_now=False)
    data_update = models.DateTimeField('Alterado',auto_now_add=False, auto_now=True)
    ativo = models.NullBooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['-id']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class GroupProduct(models.Model):
    group = models.CharField('Grupo', max_length=50, unique=True)
    desc = models.TextField('Descrição', null=True, blank=True)

    class Meta:
        ordering = ['group']
        verbose_name = 'Grupo de Produto'
        verbose_name_plural ='Grupos de Produtos'

    def __str__(self):
        return self.group

