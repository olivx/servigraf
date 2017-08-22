from django.contrib.auth.models import User
from django.test import TestCase
from django.shortcuts import resolve_url as r


class TestViewProduct(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveiravicente.net@gmail.com')
        user.set_password('logan277')
        user.save()
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


class TestCreateViewGet(TestCase):

    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveiravicente.net@gmail.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')
        self.rep =  self.client.get(r('catalogo:product_create'))

    def test_get(self):
        """status code 200"""
        self.assertEqual(200, self.rep.status_code)

    def test_template_user(self):
        """Template used must be product_modal_save"""
        self.assertTemplateUsed(self.rep , 'product_modal_save.html')

    def test_html(self):
        content = [
            (4, '<button '),
            (2, '<textarea '),
            (3, '<select '),
            (2, 'id_nome'),
        ]

        for count, expected in content:
            with self.subTest():
                self.assertContains(self.rep, expected, count)

