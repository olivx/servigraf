from django.core.exceptions import ValidationError
from django.test import TestCase
from django.forms import model_to_dict
from model_mommy import mommy

from core.forms import ClientForm
from core.models import Cliente


def get_data(model):
    return model_to_dict(model, fields=[field.name for field in model._meta.fields])


def get_model(tipo=1, documento='09081524000129', razao_social='Servigraf LTDA', nome_fantasia='servigraf'):
    return mommy.make(Cliente, razao_social=razao_social, nome_fantasia=nome_fantasia,
                      tipo=tipo, documento=documento, observacao=' ', ramo='grafico')


def get_form_erros(form, field):
    return form.errors.as_data()[field][0].code


def data_upper(data, field):
    return data[field].upper()


class TestClientFormCNPJValido(TestCase):
    def setUp(self):
        self.data = get_data(get_model())
        self.form = ClientForm(data=self.data)

    def test_is_valid(self):
        """Test if cnpj without formatter is valid """
        self.assertTrue(self.form.is_valid())


class TestFormClientCPF(TestCase):
    def setUp(self):
        self.data = self.data = get_data(get_model(tipo=2, documento='32283627877'))
        self.form = ClientForm(self.data)

    def test_cpf_is_valid(self):
        """CPF and tipo == 2 must be valid """
        self.assertTrue(self.form.is_valid())


class TestClientFormCPFInvalid(TestCase):
    def setUp(self):
        self.data = self.data = get_data(get_model(tipo=2, documento='11122233366'))
        self.form = ClientForm(self.data)
        self.error = self.form.errors.as_data()['__all__'][0]

    def test_tipo_documento_is_valid(self):
        """Test is invalid CNPJ if tipo is  CPF"""
        self.assertFalse(self.form.is_valid())

    def test_error_code_invalid(self):
        '''The error code must be CPF_INVALIDO'''
        self.assertEqual(self.error.code, 'CPF_INVALIDO')

    def test_erro_code_required(self):
        """The CPF J must be required """
        self.data['documento'] = ''
        form = ClientForm(self.data)
        self.assertEqual(get_form_erros(form, '__all__'), 'CPF_REQUIRED')


class TestClientFormCNPJInvalido(TestCase):
    def setUp(self):
        self.data = self.data = get_data(get_model(documento='112223330000155'))
        self.form = ClientForm(self.data)
        self.form.is_valid()

    def test_is_invalid_document(self):
        """Test if documento is invalid """
        self.assertFalse(self.form.is_valid())

    def teste_erro_code_invalid_cnpj(self):
        """The error code must be CNPJ_INVALIDO"""
        self.assertEqual(get_form_erros(self.form, '__all__'), 'CNPJ_INVALIDO')

    def test_erro_code_required(self):
        """The CNPJ must be required """
        self.data['documento'] = ''
        form = ClientForm(self.data)
        self.assertEqual(get_form_erros(form, '__all__'), 'CNPJ_REQUIRED')


class TestRazaoSocial_NomeFantasia(TestCase):
    def setUp(self):
        self.data = self.data = get_data(get_model(tipo=2, documento='32283627877'))
        self.data_invalid = get_data(get_model(tipo=2, documento='32283627877', razao_social='th', nome_fantasia='th'))
        self.form = ClientForm(self.data)
        self.form.is_valid()

    def test_razao_social_upper_cause(self):
        self.assertEqual(data_upper(self.data, field='razao_social'), self.form.cleaned_data['razao_social'])

    def test_nome_fantasia_upper_case(self):
        self.assertEqual(data_upper(self.data, field='nome_fantasia'), self.form.cleaned_data['nome_fantasia'])

    def test_more_than_3_razao_social(self):
        form = ClientForm(self.data_invalid)
        self.assertEqual(get_form_erros(form, 'razao_social'), 'MIN_3')

    def test_more_than_3_nome_fantasia(self):
        form = ClientForm(self.data_invalid)
        self.assertEqual(get_form_erros(form, 'nome_fantasia'), 'MIN_3')
