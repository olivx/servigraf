import json

from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.test import TestCase
from django.shortcuts import resolve_url as r
from django.contrib.messages import get_messages, get_level
from model_mommy import mommy

from catalogo.models import Produto, GroupProduct


def _get_user():
    _user_name = 'olvx'
    _password = 'logan277'
    user = User.objects.create(username=_user_name, email='oliveiravicente.net@gmail.com')
    user.set_password(_password)
    user.save()


class TestViewProduct(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        self.resp = self.client.get(r('catalogo:product_list'))

    def test_get(self):
        """Test status code 200 for get product """
        self.assertEqual(200, self.resp.status_code)

    def test_template_in_use(self):
        """Template in use must be product_list.html"""
        self.assertTemplateUsed(self.resp, 'product_list.html')

    def test_html(self):
        content = [
            (1, '<table'),
            (1, '<button id="product-create"'),
            (1, '<tbody'),
            (1, 'Não há resultados'),
            (2, '<div class="modal-dialog')
        ]

        for count, expected in content:
            with self.subTest():
                self.assertContains(self.resp, expected, count)


class TestCreateProductGet(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        self.resp = self.client.get(r('catalogo:product_create'))

    def test_get(self):
        """status code 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template_user(self):
        """Template used must be product_modal_save"""
        self.assertTemplateUsed(self.resp, 'product/product_modal_save.html')

    def test_html(self):
        content = [
            (4, '<button '),
            (2, '<textarea '),
            (3, '<select '),
            (2, 'id_nome'),
        ]

        for count, expected in content:
            with self.subTest():
                self.assertContains(self.resp, expected, count)


class TestCreateProductPost(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        data = dict(nome='produto nome', desc='desc produto', tipo=1, valor=1.00, obs='obs produto',
                    quantidade=1)
        self.resp = self.client.post(r('catalogo:product_create'), data)

    def test_create(self):
        """Product must be created """
        self.assertEqual(1, Produto.objects.count())

    def test_form_is_valid(self):
        """is_form_valid must be True"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertEqual(True, _json_response['is_form_valid'])

    def test_has_html_table(self):
        """html_table must be True"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue(_json_response['html_table'])

    def test_message(self):
        """must have message success"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue('alert-success' in _json_response['message'])


class TestCreateProductInvalidPost(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        data = dict(nome='', desc='desc produto', tipo=1, valor=1.00, obs='obs produto',
                    quantidade=1)
        self.resp = self.client.post(r('catalogo:product_create'), data)

    def test_not_create(self):
        """Product don't must be created """
        self.assertEqual(0, Produto.objects.count())

    def test_form_is_invalid(self):
        """is_form_valid must be False"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertEqual(False, _json_response['is_form_valid'])

    def test_has_html_table(self):
        """html_table must be True"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue(_json_response['html_form'])

    def test_message(self):
        """must have message success"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue('alert-danger' in _json_response['message'])


class TestUpdateProductPost(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        self.prod = mommy.make(Produto, nome='produto nome', desc='desc produto',
                               tipo=1, valor=1.00, obs='obs produto', quantidade=1)
        data = dict(nome='produto nome alterado', desc='desc produto', tipo=1, valor=1.00, obs='obs produto',
                    quantidade=1)
        self.resp = self.client.post(r('catalogo:product_update', pk=self.prod.id), data)

    def test_form_is_valid(self):
        """is_form_valid must be True"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertEqual(True, _json_response['is_form_valid'])

    def test_has_html_table(self):
        """html_table must be True"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue(_json_response['html_table'])

    def test_message(self):
        """must have message success"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue('alert-warning' in _json_response['message'])


class TestupdateProductInvalidPost(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        self.prod = mommy.make(Produto, nome='produto', desc='desc produto', tipo=1, valor=1.00, obs='obs produto',
                               quantidade=1)
        data = dict(nome='', desc='desc produto', tipo=1, valor=1.00, obs='obs produto',
                    quantidade=1)
        self.resp = self.client.post(r('catalogo:product_update', pk=self.prod.id), data)

    def test_form_is_invalid(self):
        """is_form_valid must be False"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertEqual(False, _json_response['is_form_valid'])

    def test_has_html_table(self):
        """html_table must be True"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue(_json_response['html_form'])

    def test_message(self):
        """must have message success"""
        _json_response = json.loads(self.resp.content.decode('utf-8'))
        self.assertTrue('alert-danger' in _json_response['message'])


class TestDeleteProductPost(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        self.prod = mommy.make(Produto, nome='produto nome', desc='desc produto',
                               tipo=1, valor=1.00, obs='obs produto', quantidade=1)
        self.resp = self.client.post(r('catalogo:product_delete', pk=self.prod.id))

    def test_count_model(self):
        """must have  zero model """
        self.assertEqual(0, Produto.objects.count())

    def test_status_code(self):
        """Page must be recdirect """
        self.assertEqual(302, self.resp.status_code)


class TestListGrouProdct(TestCase):
    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        mommy.make(GroupProduct, _quantity=10)
        self.resp = self.client.get(r('catalogo:group_list'))

    def test_status_code(self):
        """status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

class TestGroupProductGet(TestCase):

    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        data = dict(group='group name', desc='desc group')
        self.resp = self.client.get(r('catalogo:group_create'), data)

    def get_json(self):
        return json.loads(self.resp.content.decode('utf-8'))

    def test_status_code(self):
        """status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        """template in used must be group_modal_save.html"""
        self.assertTemplateUsed(self.resp, 'group/group_modal_save.html')

    def test_josn(self):
        """test json has html_table , message html_form"""
        json_resp = self.get_json()
        with self.subTest():
            self.assertTrue(json_resp['message'])
            self.assertTrue(json_resp['html_form'])
            self.assertTrue(json_resp['html_table'])

    def test_message(self):
        json_resp = self.get_json()
        with self.subTest():
            self.assertTrue('alert-warning' in json_resp['message'])
            self.assertTrue('Contate um administrador. para efutar a operação.' in json_resp['message'])

class TestGroupProductPostValid(TestCase):

    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        data = dict(group='group name', desc='desc group')
        self.resp = self.client.post(r('catalogo:group_create'), data)

    def get_json(self):
        return json.loads(self.resp.content.decode('utf-8'))

    def test_status_code(self):
        """status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        """template in used must be group_modal_save.html"""
        self.assertTemplateUsed(self.resp, 'group/group_modal_save.html')

    def test_josn(self):
        """test json has html_table , message html_form"""
        json_resp = self.get_json()
        with self.subTest():
            self.assertTrue(json_resp['message'])
            self.assertTrue(json_resp['html_form'])
            self.assertTrue(json_resp['html_table'])
            self.assertEqual(True, json_resp['is_form_valid'])

    def test_message(self):
        json_resp = self.get_json()
        with self.subTest():
            self.assertTrue('alert-success' in json_resp['message'])
            self.assertTrue('Adicionado com Sucesso' in json_resp['message'])


    def test_count(self):
        """must have 1 group poroduct"""
        self.assertEqual(1, GroupProduct.objects.count())


class TestGroupProductPostInvalid(TestCase):

    def setUp(self):
        _get_user()
        self.client.login(username='olvx', password='logan277')
        data = dict(group='', desc='desc group')
        self.resp = self.client.post(r('catalogo:group_create'), data)

    def get_json(self):
        return json.loads(self.resp.content.decode('utf-8'))

    def test_status_code(self):
        """status code must be 200"""
        self.assertEqual(200, self.resp.status_code)

    def test_template_used(self):
        """template in used must be group_modal_save.html"""
        self.assertTemplateUsed(self.resp, 'group/group_modal_save.html')

    def test_josn(self):
        """test json has html_table , message html_form"""
        json_resp = self.get_json()
        with self.subTest():
            self.assertTrue(json_resp['message'])
            self.assertTrue(json_resp['html_form'])
            self.assertTrue(json_resp['html_table'])
            self.assertEqual(False, json_resp['is_form_valid'])

    def test_message(self):
        json_resp = self.get_json()
        with self.subTest():
            self.assertTrue('alert-danger' in json_resp['message'])
            self.assertTrue('Formulario invalido, verifique as inconsistências apontada a baixo' in
                            json_resp['message'])


    def test_count(self):
        """must have 1 group poroduct"""
        self.assertEqual(0, GroupProduct.objects.count())



