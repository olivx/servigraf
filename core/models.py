from django.db import models
from django.shortcuts import resolve_url as r

from core.manager import ContatoManager, EnderecoManager


class Timestamp(models.Model):
    class Meta:
        abstract = True

    criado_em = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modificado_em = models.DateTimeField(auto_now_add=False, auto_now=True, null=True)

class EntidadeAbstract(Timestamp):
    nome_fantasia = models.CharField('Nome Fantasia', max_length=255, blank=False, null=False)
    razao_social = models.CharField('Razão Social', max_length=255, blank=False, null=False)
    observacao = models.TextField('Descrição', blank=True, null=False)
    documento = models.CharField('CNPJ', max_length=30, blank=True, null=False)
    ativo  = models.NullBooleanField('Ativo', default=True)

    def __str__(self):
        return self.nome_fantasia

    class Meta:
        abstract = True

class ContatoAstract(models.Model):
    nome = models.CharField(max_length=70)
    sobre_nome = models.CharField(max_length=70)
    observacao = models.TextField('observação', null=True, blank=True)
    ativo = models.BooleanField(default=True)


    objects = ContatoManager()

    def __str__(self):
        return '%s %s'%(self.nome, self.sobre_nome)

    class Meta:
        ordering = ['-id']
        abstract = True
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

class Cliente(EntidadeAbstract):
    TIPO_JURIDICO = 1
    TIPO_FISICO = 2
    TIPO_CLIENTE = (
        (TIPO_JURIDICO, 'Juridico'),
        (TIPO_FISICO, 'Fisico'),
    )

    user = models.ForeignKey('auth.User', blank=True, null=True, related_name='cli_user')
    tipo = models.SmallIntegerField('Fisico/Juridico', choices=TIPO_CLIENTE,
                                            default=TIPO_JURIDICO, blank=False, null=False)
    ramo = models.CharField('Ramo', max_length=100, blank=True, null=False)
    mensalista = models.BooleanField(default=False)

    class Meta:
        ordering =  ['-id']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome_fantasia

    def get_absolute_url(self):
        return r('servigraf:detail_client', pk=self.pk)

class Email(Timestamp):
    email = models.EmailField('E-mail', max_length=70)
    contato = models.ForeignKey('core.Contato', related_name='emails', null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'E-mail'
        verbose_name_plural = 'E-mails'

class Telefone(Timestamp):
    FIXO = 1
    FAX = 2
    CASA = 3
    TRABALHO = 4
    CELULAR = 5
    CELULAR_TIM = 6
    CELULAR_CLARO = 7
    CELULAR_VIVO = 8
    CELULAR_OI = 9
    TIPO_TELEFONE = (
        (CELULAR_OI,    'OI'),
        (CELULAR_TIM,   'TIM'),
        (FAX,           'FAX'),
        (FIXO,          'FIXO'),
        (CELULAR_VIVO,  'VIVO'),
        (CASA,          'CASA'),
        (CELULAR_CLARO, 'CLARO'),
        (CELULAR,       'CELULAR'),
        (TRABALHO,      'TRABALHO'),
    )

    telefone = models.CharField('Telefone', max_length=15)
    tipo = models.PositiveIntegerField('Tipo', choices=TIPO_TELEFONE, default=FIXO)
    contato = models.ForeignKey('core.Contato', related_name='telefones', null=True, blank=True)

    def __str__(self):
        _fixo =[self.FIXO, self.FAX, self.TRABALHO, self.CASA]
        if self.tipo in _fixo:
            return '{} {}-{}'.format(self.telefone[:3], self.telefone[3:7], self.telefone[-4:])
        return '{} {}-{}'.format(self.telefone[:3], self.telefone[3:8], self.telefone[-4:])

    class Meta:
        verbose_name = 'Telefone'
        verbose_name_plural = 'Telefones'

class Contato(ContatoAstract):
    cliente = models.ForeignKey('core.Cliente', related_name='contatos' , blank=True, null=True)

class Endereco(models.Model):
    RESIDENCIAL = 1
    COMERCIAL = 2
    ENTERGA = 3
    FATURAMENTO = 4

    TIPO_ENDERECO = (
        (RESIDENCIAL, 'Resindencial'),
        (COMERCIAL, 'Comercial'),
        (ENTERGA, 'Entrega'),
        (FATURAMENTO, 'Faturamento'),
    )

    cliente = models.ForeignKey('core.Cliente', related_name='enderecos')

    logradouro = models.CharField('Logradouro', max_length=50)
    endereco = models.CharField('Endereço', max_length=60)
    numero = models.PositiveIntegerField("Numero")
    complemento = models.CharField('Complemento', max_length=40, null=True, blank=True)
    cep = models.CharField('Cep', max_length=11)
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    uf = models.CharField('UF', max_length=20)
    tipo_end = models.PositiveIntegerField('Tipo Endereço', choices=TIPO_ENDERECO, default=COMERCIAL)
    observacao = models.TextField(null=True, blank=True)
    ativo = models.BooleanField(default=True)

    objects = EnderecoManager()

    def __str__(self):
        return '{0} {1}, {2} {3}'.format(
            self.logradouro, self.endereco, self.numero , self.complemento
        ).upper()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'