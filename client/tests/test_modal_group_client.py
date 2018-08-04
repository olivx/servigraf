from django.test import TestCase
from model_mommy import mommy
from django.utils import timezone as datetime

# Create your tests here.
from django.contrib.auth.models import User
from client.models import CatalogoGrupo, GrupoCliente, StatusTrail, Ticket, TicketItem

class TestGroupClient(TestCase):

    def setUp(self):
        user =  mommy.make('auth.User')
        self.client_group =  mommy.make('client.GrupoCliente', users=mommy.make('auth.User', _quantity=10),
                                        clientes=mommy.make('core.Cliente', _quantity=2))

        # produtos
        self.prod_1 = mommy.make('catalogo.Produto')
        self.prod_2 = mommy.make('catalogo.Produto')
        self.prod_3 = mommy.make('catalogo.Produto')

        # create catalogo
        CatalogoGrupo.objects.create(grupo=self.client_group, produto=self.prod_1, valor=1.20, owner=user)
        CatalogoGrupo.objects.create(grupo=self.client_group, produto=self.prod_2, valor=22.10, owner=user)
        CatalogoGrupo.objects.create(grupo=self.client_group, produto=self.prod_3, valor=10.30, owner=user)

    def test_create(self):
        '''test if group is create'''
        self.assertEqual(1, GrupoCliente.objects.count())

    def test_uuid_cant_by_none(self):
        ''' test uuid exists'''
        self.assertNotEqual(self.client_group.uuid , None)

    def test_many_clients(self):
        '''client group can by many clients'''
        self.assertEqual(self.client_group.clientes.count(), 2)

    def test_has_produto(self):
        '''grupo cliente has produto'''
        self.assertTrue(self.client_group.produtos.exists())

    def test_has_users(self):
        '''grupo cliente has users'''
        self.assertTrue(self.client_group.users.exists())

    def test_group_has_3_produto(self):
        '''group must have 3 produtos'''
        self.assertEqual(3, self.client_group.produtos.count())

    def test_pk_is_int(self):
        '''pk must be integer'''
        self.assertIsInstance(self.client_group.pk, int)

class TestStatusTrail(TestCase):
    def setUp(self):
        self.trail = mommy.make('client.StatusTrail')

    def test_create(self):
        '''create status trail'''
        self.assertTrue(StatusTrail.objects.exists())

    def test_default_value(self):
        '''default value status trail'''
        with self.subTest():
            self.assertEqual(self.trail.status, 0)
            self.assertEqual(str(self.trail), 'não liberado')

    def test_trail_cant_be_null(self):
        '''trail cant be null'''
        field =  StatusTrail._meta.get_field('ticket')
        self.assertFalse(field.null)

    def test_trail_cant_be_blank(self):
        '''trail cant be blank'''
        field =  StatusTrail._meta.get_field('ticket')
        self.assertFalse(field.blank)

    def test_trail_must_have_owner(self):
        '''trail has onwer'''
        user = self.trail.owner
        self.assertIsInstance(user, User)

class TestTicket(TestCase):
    def setUp(self):
        self.ticket = mommy.make('client.Ticket', data_entrega=datetime.now())

    def test_create(self):
        '''test if ticket exists'''
        self.assertTrue(Ticket.objects.exists())

    def test_active_true(self):
        '''test if ticket is active'''
        self.assertTrue(self.ticket.ativo)

    def test_data_saida(self):
        '''test data saida'''
        field =  Ticket._meta.get_field('data_saida')
        with self.subTest():
            self.assertTrue(field.null)
            self.assertTrue(field.blank)

    def test_data_finalizado(self):
        '''test data_finalizado'''
        field =  Ticket._meta.get_field('data_finalizado')
        with self.subTest():
            self.assertTrue(field.null)
            self.assertTrue(field.blank)

    def test_data_entrega(self):
        '''test data entrega'''
        self.assertEqual(self.ticket.data_entrega.date(), datetime.now().date())

class testTicketitem(TestCase):
    def setUp(self):
        self.ticket =  mommy.make('client.Ticket')
        self.items =  mommy.make('client.TicketItem', _quantity=10)

    def ticket_has_items(self):
        '''ticket has items'''
        self.assertTrue(self.ticket.tickets.exists())

    def ticket_has_10_items(self):
        self.assertEqual(10, self.ticket.tickets.count())

    def quantidate(self):
        ''' quantidadte cant be null or blank'''
        field =  testTicketitem._meta.get_field('quantidate')
        with self.subTest():
            self.assertFalse(field.null)
            self.assertFalse(field.blank)

    def valor(self):
        ''' quantidadte cant be null or blank'''
        field =  testTicketitem._meta.get_field('valor')
        with self.subTest():
            self.assertFalse(field.null)
            self.assertFalse(field.blank)
