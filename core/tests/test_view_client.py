from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.test import TestCase
from django.shortcuts import resolve_url as r
from model_mommy import mommy

# Create your tests here.
import json

from core.forms import ClientForm
from core.models import Cliente, Endereco, Contato


class TestViewHome(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')
        self.resp = self.client.get(r('home'))

    def test_get(self):
        """Testando o get da home"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Template em usuo para home deve ser o index.html"""
        self.assertTemplateUsed(self.resp, 'index.html')


class TesvViewClienteList(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')
        self.clients = mommy.make(Cliente, _quantity=3)
        self.resp = self.client.get(r('servigraf:clientes'))

    def test_get(self):
        """The Status  code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template_list(self):
        """Template in used must be core/client_list.html"""
        self.assertTemplateUsed(self.resp, 'clientes/client_list.html')

    def test_context(self):
        """Context must be client_list  """
        context = ['client_list']
        client_list = self.resp.context
        for key in context:
            with self.subTest():
                self.assertIn(key, 'client_list')

    def test_html(self):
        """Test Html im template list"""
        html = [
            (4, '<tr'),
            (1, 'class="btn btn-primary js-open-form-cliente'),
            (1, "servigraf/clientes/save/"),
            (1, 'glyphicon glyphicon-plus'),
            (7, '<button type="button" class="btn btn-'),
            (3, '<button type="button" class="btn btn-warning'),
            (3, '<button type="button" class="btn btn-danger'),
            (1, 'h1 class="page-header"'),
        ]

        for count, expeted in html:
            with self.subTest():
                self.assertContains(self.resp, expeted, count)


class TestViewSave(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')
        self.cli = mommy.make(Cliente, tipo=2, documento='32283627877')
        self.data = model_to_dict(self.cli, fields=[field.name for field in self.cli._meta.fields])
        self.get_resp = self.client.get(r('servigraf:save_client'))
        self.post_resp = self.client.post(r('servigraf:save_client'), self.data)

    def test_get_save(self):
        """Test get for """
        resp_dict = json.loads(self.get_resp.content.decode('utf-8'))
        self.assertTrue(resp_dict['html_form'])

    def test_pot_save(self):
        """Test is save post """
        resp_dict = json.loads(self.post_resp.content.decode('utf-8'))
        self.assertTrue('foi adicionado com sucesso!' in resp_dict['message'])
        self.assertTrue(resp_dict['is_form_valid'])
        self.assertTrue(resp_dict['html_table'])

    def test_post_save_invalid(self):
        """Test if post save retorn erro and is_form_valids equal false """
        self.data['documento'] = '12334556756'
        resp = self.client.post(r('servigraf:save_client'), self.data)
        resp_cli = json.loads(resp.content.decode('utf-8'))
        self.assertFalse(resp_cli['is_form_valid'])
        self.assertTrue('Erros foram processado durante' in resp_cli['message'])


class TestViewUpdate(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')
        self.cli = mommy.make(Cliente, razao_social='Thiago', nome_fantasia='Oliveira', tipo=2, documento='32283627877')
        self.data = dict(razao_social='Thiago', nome_fantasia='vicente', tipo=2, documento='32283627877')
        self.client.post(r('servigraf:update_client', pk=self.cli.id), self.data)

    def test_create(self):
        """Test create new client """
        self.assertEqual(1, Cliente.objects.count())

    def test_get_update(self):
        """Test update client """
        resp = self.client.get(r('servigraf:update_client', pk=self.cli.id))
        resp_dict = json.loads(resp.content.decode('utf-8'))
        key = [keys for keys, value in resp_dict.items()]
        self.assertIn(''.join(key), 'html_form')

    def test_post_update_invalid(self):
        """Test update client invalid  """
        self.data['documento'] = '112236985'
        resp = self.client.post(r('servigraf:update_client', pk=self.cli.id), self.data)
        resp_dict = json.loads(resp.content.decode('utf-8'))
        self.assertFalse(resp_dict['is_form_valid'])
        self.assertTrue('Erros foram processado' in resp_dict['message'])

    def test_post_update_valid(self):
        """Test update client valid"""
        self.data['tipo'] = 1
        self.data['documento'] = '09.081.524/0001-29'
        resp = self.client.post(r('servigraf:update_client', pk=self.cli.id), self.data)
        resp_dict = json.loads(resp.content.decode('utf-8'))
        self.assertTrue(resp_dict['is_form_valid'])


class TestViewDelete(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')
        self.cli = mommy.make(Cliente, tipo=2, documento='32283627877')
        self.data = model_to_dict(self.cli, fields=[field.name for field in self.cli._meta.fields])
        self.get_resp = self.client.get(r('servigraf:delete_client', pk=self.cli.id))
        self.post_resp = self.client.post(r('servigraf:delete_client', pk=self.cli.id))

    def test_get_delete(self):
        """Test get for """
        resp_dict = json.loads(self.get_resp.content.decode('utf-8'))
        self.assertTrue(resp_dict['html_form'])

    def test_post_delete(self):
        """Test is save post """
        resp_dict = json.loads(self.post_resp.content.decode('utf-8'))
        self.assertTrue('para reativa-lo você precisa usar a area administrativa.' in resp_dict['message'])
        self.assertTrue(resp_dict['is_form_valid'])
        self.assertTrue(resp_dict['html_table'])


class TestViewFormClient(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')
        self.resp = self.client.get(r('servigraf:save_client'))

    def test_get(self):
        """Status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        """Template used must be clientes/clint_form.html"""
        self.assertTemplateUsed(self.resp, 'clientes/client_form.html')

    def test_contex_form(self):
        """context form must be ClientForm"""
        form = self.resp.context['form_client']
        self.assertIsInstance(form, ClientForm)

    def test_html(self):
        """Test Html in template """
        html = [
            (1, 'checkbox'),
            (6, '<input'),
            (1, '<select'),
            (1, 'Cadastro de Cliente'),
            (1, 'Salvar'),
            (1, 'Fechar'),
            (3, '<button'),
            (3, '<button'),

        ]
        for count, expeted in html:
            with self.subTest():
                self.assertContains(self.resp, expeted, count)


class TestClienteDetail(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')

        self.cli = mommy.make(Cliente, nome_fantasia='cliente servigraf')
        self.end = mommy.make(Endereco, endereco='rua do cliente', ativo=True)
        self.end2 = mommy.make(Endereco, endereco='rua 2 do cliente', ativo=False)

        self.contato = mommy.make(Contato, nome='contato do cliente', ativo=True)
        self.contato2 = mommy.make(Contato, nome='outro contato', ativo=False)

        self.cli.enderecos.add(self.end)
        self.cli.enderecos.add(self.end2)

        self.cli.contatos.add(self.contato)
        self.cli.contatos.add(self.contato2)
        # self.data =  model_to_dict(self.cli, fields=[fields.name for fields in self.cli._meta.fields])
        self.resp = self.client.get(r('servigraf:detail_client', self.cli.id))

    def test_get(self):
        """Test cliente detail get"""
        self.assertEqual(200, self.resp.status_code)

    def test_contato_all(self):
        """Cliente must have 2 contacts """
        self.assertEqual(2, Contato.objects.count())

    def test_contatos_ativos(self):
        """cliente must hav 1 contact ativo"""
        self.assertEqual(1, Contato.objects.ativos().count())

    def test_endereco_all(self):
        """Cliente must have 2 end """
        self.assertEqual(2, Endereco.objects.count())

    def test_endereco_ativos(self):
        """cliente must hav 1 end ativo"""
        self.assertEqual(1, Endereco.objects.ativos().count())

