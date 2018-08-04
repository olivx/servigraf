from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class ModelBase(models.Model):

    owner =  models.ForeignKey(settings.AUTH_USER_MODEL)
    criado_em = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modificado_em = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

    class Meta:
        abstract = True

class CatalogoGrupo(ModelBase):

    grupo =  models.ForeignKey('client.GrupoCliente')
    produto = models.ForeignKey('catalogo.Produto')
    valor =  models.DecimalField('Valor', decimal_places=2, max_digits=10)

    def __str__(self):
        return self.grupo.title

class GrupoCliente(ModelBase):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title =  models.CharField(max_length=200)
    clientes =  models.ManyToManyField('core.Cliente', related_name='cgroups')
    produtos = models.ManyToManyField('catalogo.Produto', through='client.CatalogoGrupo')
    users =  models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_groups')

    def __str__(self):
        return self.title

class StatusTrail(ModelBase):

    AGUARDANDO_LIEBRACAO = 0
    PRODUCAO = 1
    LIBERADO = 2
    LIBERADO_PRODUCAO = 3
    SEPARACAO = 4
    TERMINADO = 5

    choices_list =  (
        (AGUARDANDO_LIEBRACAO , 'não liberado'),
        (PRODUCAO , 'em produção'),
        (LIBERADO , 'liberado'),
        (LIBERADO_PRODUCAO , 'liberado produção'),
        (SEPARACAO , 'separação'),
        (TERMINADO , 'finalizado'),
    )

    ticket = models.ForeignKey('client.Ticket', related_name='ticket_trails')
    status =  models.PositiveSmallIntegerField('Status', choices=choices_list, default=AGUARDANDO_LIEBRACAO)

    def __str__(self):
        return self.get_status_display()

class Ticket(ModelBase):

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cliente =  models.ForeignKey('core.Cliente')
    ativo =  models.BooleanField(default=True)
    data_entrega = models.DateTimeField()

    data_finalizado = models.DateTimeField(null=True, blank=True)
    data_saida =  models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.pk)

class TicketItem(models.Model):
    ticket =  models.ForeignKey('client.Ticket', related_name='tickets')
    produto =  models.ForeignKey('catalogo.Produto')
    quantidate =  models.IntegerField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
