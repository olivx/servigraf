from django.test import TestCase
from django.shortcuts import resolve_url as r
class TestViewProduct(TestCase):

    def setUp(self):
        self.resp =  self.client.get(r('catalogo:product_list'))

    def test_get(self):
        """Test status code 200 for get product """
        self.assertEqual(200, self.resp.status_code)