from django.test import TestCase

from catalogo.forms import ProductForm, GroupProductForm


class TestFormProduct(TestCase):

    def test_form_is_valid(self):
        """Valid form"""
        self.assertEqual(self.make_validation_form().is_valid(), True)

    def test_nome_not_null(self):
        """Nome not must be null"""
        form = self.make_validation_form(nome='')
        self.assertEqual(form.is_valid(), False)

    def test_quantidade_must_be_big_than_zero(self):
        """quantidade must be biger than zero"""
        form = self.make_validation_form(quantidade=-1)
        form.is_valid()
        self.assertEqual(0 , form.cleaned_data.get('quantidade'))

    def test_quantidade_None_default_zero(self):
        """quantidade if is none zero is default """
        form = self.make_validation_form(quantidade=None)
        form.is_valid()
        self.assertEqual(0, form.cleaned_data.get('quantidade'))

    def test_valor_biger_than_zero(self):
        """valor must be giger then zero"""
        form =  self.make_validation_form(valor=0)
        form.is_valid()
        self.assertListEqual(['valor'] , list(form.errors))

    def test_tipo(self):
        """Tipo can be only 1 or 2"""
        list_tipo =  [ 0, 3, 4, 5, 6, 8, 9]
        for tipo in list_tipo:
            with self.subTest():
                form = self.make_validation_form(tipo=tipo)
                form.is_valid()
                self.assertFalse(form.is_valid())


    def make_validation_form(self, **kwargs):
        valid = dict(nome='produto', desc='descrição produto' , tipo=1 ,
                     quantidade=1, valor=1.00, ativo=True, obs='observação do produto')

        data =  dict(valid, **kwargs)
        form = ProductForm(data)
        return form

class TestFromGroupProduct(TestCase):

    def make_form_valid(self, **kwargs):
        valid = dict(group='produto valiado', desc='desc produto valido')
        data = dict(valid, **kwargs)
        form = GroupProductForm(data)
        form.is_valid()
        return form


    def test_form_group_invalid(self):
        """Group Product From must have a group name """
        form = self.make_form_valid(group='')
        self.assertEqual(False, form.is_valid())