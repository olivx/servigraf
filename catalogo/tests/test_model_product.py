from django.test import TestCase
from catalogo.models import Produto, GroupProduct
from model_mommy import mommy

# Create your tests here.
class TestModelProduto(TestCase):

    def setUp(self):
        self.prod = mommy.make(Produto)
        self.group = mommy.make(GroupProduct, group='Test Produto')
        self.prod.group = self.group
        self.prod.save()


    def get_field(self, field, klass=Produto):

        return klass._meta.get_field(field)

    def test_desc_can_be_null(self):
        """Desc is must be not  null"""
        self.assertTrue(self.get_field('desc').blank)

    def test_create(self):
        """Test if exists"""
        self.assertTrue(Produto.objects.exists())

    def test_create_one(self):
        """Test if there are only one"""
        self.assertEqual(Produto.objects.count(), 1)

    def test_ativo_isTrue(self):
        """Test if ativo is true default"""
        self.assertTrue(self.prod.ativo)

    def test_default_tipo(self):
        """Default tipo must be produto = 1 """
        self.assertEqual(self.prod.tipo, Produto.PRODUTO)

    def test_group_blank(self):
        """Grupo must be blank"""
        self.assertTrue(self.get_field("group").blank)

    def test_must_have_group(self):
        """produto may have a group instance """
        self.assertIsInstance(self.prod.group , GroupProduct)

    def test_has_group(self):
        """test if has a group Test Produto"""
        self.assertTrue(Produto.objects.first().group)

    def test_str_produto(self):
        """Test if str is nome """
        self.assertEqual(self.prod.__str__(), self.prod.nome)

    def test_str_group(self):
        """Test if str is nome"""
        self.assertEqual(self.group.__str__(), self.group.group)

    def test_group_desc_blank(self):
        """Test group produto desc can be blank """
        self.assertTrue(self.get_field("desc", klass=GroupProduct).blank)

    def test_datecreated(self):
        """test if have date create and date update is null"""
        self.assertTrue(self.prod.data_create)

