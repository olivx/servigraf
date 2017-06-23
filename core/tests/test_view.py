from django.forms import model_to_dict
from django.test import TestCase
from django.shortcuts import resolve_url as r
from model_mommy import mommy

# Create your tests here.
import json

from core.forms import ClientForm
from core.models import Cliente


class TestViewHome(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('home'))

    def test_get(self):
        """Testando o get da home"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Template em usuo para home deve ser o index.html"""
        self.assertTemplateUsed(self.resp, 'index.html')


class TesvViewClienteList(TestCase):
    def setUp(self):
        self.clients = mommy.make(Cliente, _quantity=3)
        self.resp = self.client.get(r('servigraf:clientes'))

    def test_get(self):
        '''The Status  code must be 200'''
        self.assertEqual(200, self.resp.status_code)

    def test_template_list(self):
        '''Template in used must be core/client_list.html'''
        self.assertTemplateUsed(self.resp, 'clientes/client_list.html')

    def test_context(self):
        '''Context must be client_list  '''
        context = ['client_list']
        client_list = self.resp.context
        for key in context:
            with self.subTest():
                self.assertIn(key, 'client_list')

    def test_html(self):
        html = [
            (4, '<tr'),
            (1, 'class="btn btn-primary js-open-form-cliente'),
            (1, "servigraf/clientes/save/"),
            (1, 'glyphicon glyphicon-plus'),
            (7, '<button type="button" class="btn btn-'),
            (3, '<button type="button" class="btn btn-warning'),
            (3, '<button type="button" class="btn btn-danger'),
            (1, 'div class="page-header"'),
        ]

        for count, expeted in html:
            with self.subTest():
                self.assertContains(self.resp, expeted, count)


class TestViewUpdate(TestCase):
    def setUp(self):
        self.cli = Cliente(razao_social='Thiago', nome_fantasia='Oliveira', tipo=2, documento='32283627877')
        self.data = model_to_dict(self.cli, fields=[field.name for field in self.cli._meta.fields])
        self.client.post(r('servigraf:save_client'), self.data)

    def test_create(self):
        '''Test create new client '''
        self.assertEqual(1, Cliente.objects.count())

    def test_get_update(self):
        '''Test update client '''
        resp = self.client.get(r('servigraf:update_client', 1))
        resp_dict = json.loads(resp.content.decode('utf-8'))
        key = [keys for keys, value in resp_dict.items()]
        self.assertIn(''.join(key), 'html_form')

    def test_post_update_invalid(self):
        '''Test update client invalid  '''
        self.data['documento'] = '112236985'
        resp = self.client.post(r('servigraf:update_client', 1), self.data)
        resp_dict = json.loads(resp.content.decode('utf-8'))
        self.assertFalse(resp_dict['is_form_valid'])
        self.assertTrue('Erros foram processado' in resp_dict['message'])

    def test_post_update_valid(self):
        '''Test update client valid'''
        self.data['tipo'] =  1
        self.data['documento'] = '09.081.524/0001-29'
        resp = self.client.post(r('servigraf:update_client', 1), self.data)
        resp_dict = json.loads(resp.content.decode('utf-8'))
        self.assertTrue(resp_dict['is_form_valid'])



class TestViewFormClient(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('servigraf:save_client'))

    def test_get(self):
        '''Status code must be 200'''
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        '''Template used must be clientes/clint_form.html'''
        self.assertTemplateUsed(self.resp, 'clientes/client_form.html')

    def test_contex_form(self):
        '''context form must be ClientForm'''
        form = self.resp.context['form_client']
        self.assertIsInstance(form, ClientForm)

    def test_html(self):
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
