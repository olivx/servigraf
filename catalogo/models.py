from django.db import models


# Create your models here.


class Produto(models.Model):
    PRODUTO = 1
    SERVICO = 2
    TIPO = [
        (PRODUTO, 'produto'),
        (SERVICO, 'serviço')
    ]

    grupo = models.ForeignKey('catalogo.GrupoProduto', null=True, blank=True, related_name='grupos')

    nome = models.CharField('Nome', max_length=100)
    desc = models.TextField('Descrição', blank=True, null=True)
    tipo = models.PositiveIntegerField('Tipo', default=PRODUTO)
    valor = models.DecimalField('Valor', max_digits=10, decimal_places=3)
    obs = models.TextField('Observação', null=True, blank=True)
    quantidade = models.IntegerField('Quantidade')
    data_create = models.DateTimeField('Criado', auto_now_add=True, auto_now=False)
    data_update = models.DateTimeField('Alterado',auto_now_add=False, auto_now=True)
    ativo = models.NullBooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['-id']
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class GrupoProduto(models.Model):
    grupo = models.CharField('Grupo', max_length=50)
    desc = models.TextField('Descrição', null=True, blank=True)

    def __str__(self):
        return self.grupo
