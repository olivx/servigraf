from django.contrib.auth.models import User

from core.models import Cliente, Endereco, Email, Telefone, Contato
from django.test import TestCase
from model_mommy import mommy
import datetime


class TestModelCliente(TestCase):

    def setUp(self):
        self.cliente = Cliente.objects.create(nome_fantasia='Servigraf',
                                              razao_social='Servigraf produto e serviços LTDA',
                                              documento='111.222.333/0001-00',tipo=Cliente.TIPO_JURIDICO,
                                              observacao='Observacao sobre algo da empresa',
                                              ramo='Grafica', mensalista=True)

        self.cliente.user = User.objects\
            .create(username='olivx', email='oliveiravicnete.net@gmail.com', password='logan277')

        self.cliente.contatos.create(nome='Thiago Oliveira', sobre_nome='Vicente',
                                              observacao='Cliente antigo milis anos manolo')

        self.cliente.enderecos.create(logradouro='Rua',endereco='Domingos Ricci',numero=21,
                                 complemento='apartamento',cep='09550-080', bairro='Barcelona' ,
                                 cidade='São Caetano do Sul',uf='São Paulo - SP')

    def test_create(self):
        """Teste criando objeto no banco"""
        self.assertTrue(Cliente.objects.exists())

    def test_juridico_is_tipo_default(self):
        """Teste o cliente tipo defaul deve ser jurido"""
        self.assertEqual(1, self.cliente.tipo)

    def test_datetime_default(self):
        """Teste comparar data"""
        self.assertEqual(self.cliente.criado_em, datetime.date.today())

    def test_cliente_contato(self):
        """Teste cliente deve ter um cantato"""
        self.assertEqual(1, Cliente.objects.count())

    def test_cliente_endereco_has_one(self):
        '''Cliente precisa ter um endereço pelo menos'''
        self.assertEqual(1, Endereco.objects.count())

    def test_endereco_default_is_comercial(self):
        '''O tipo de endereço default deve ser o comercial'''
        self.assertEqual(2, self.cliente.enderecos.first().tipo_end)

    def test_contato_cliente_has_more_than_one_email(self):
        '''O contato de um cliente pode ter mais de um email '''
        Email.objects.create(email='oliveiravicente.net@gmail.com', contato=self.cliente.contatos.first())
        Email.objects.create(email='thiago@techcd.com.br', contato=self.cliente.contatos.first())
        self.assertEqual(2, Contato.objects.first().emails.count())

    def test_contato_cliente_more_than_one_telefone(self):
        '''O contato pode possuir mais de um telefone'''
        Telefone.objects.create(telefone='4232-4522', tipo=Telefone.FIXO,
                                       contato=self.cliente.contatos.first())
        Telefone.objects.create(telefone='4232-4521', tipo=Telefone.FIXO,
                                       contato=self.cliente.contatos.first())
        self.assertEqual(2, Contato.objects.first().telefones.count())

    def test_telefone_tipo_default_is_fixo(self):
        '''O tipo de telefone fixo deve ser default'''
        contato_telefone = Telefone.objects.create(telefone='4352-2010')
        self.assertEqual(Telefone.FIXO, contato_telefone.tipo)

    def test_string_telefone(self):
        '''Test se o __str__ é o mesmo do telefone '''
        self.telefone = mommy.make(Telefone, telefone='42314522')
        self.celular = mommy.make(Telefone, telefone='970513508')
        self.assertEqual('4231-4522', self.telefone.__str__())

    def test_email_string(self):
        '''Test se __str__ é o email '''
        self.email =  mommy.make(Email, email='oliveiravicente.net@gmail.com')
        self.assertEqual(self.email.__str__(), 'oliveiravicente.net@gmail.com')

    def test_cliente_string(self):
        self.cliente = mommy.make(Cliente, nome_fantasia='um qualquer cliente')
        self.assertEqual(self.cliente.__str__(), self.cliente.nome_fantasia)

    def test_contato_string(self):
        self.contato = mommy.make(Contato, nome='um qualquer cliente')
        self.assertEqual(self.contato.__str__(), '%s %s'%(self.contato.nome, self.contato.sobre_nome))












