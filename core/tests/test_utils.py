from django.test import TestCase
from re import findall
from core import utils
class TestUtils(TestCase):

    def setUp(self):
        self.valid_cnpj = '09.081.524/0001-29'
        self.valid_cpf =  '322.836.278-77'

    def test_is_cnpj(self):
        """Check is cnpj"""
        self.assertTrue(utils.is_cpf_or_cnpj(self.valid_cnpj), 'CNPJ')

    def test_is_cnpj(self):
        """Check is CPF"""
        self.assertTrue(utils.is_cpf_or_cnpj(self.valid_cpf), 'CPF')

    def test_valid_cpf(self):
        """Valid cpf """
        self.assertEqual(utils.validar_cpf(self.valid_cpf), ''.join(findall('\d+', self.valid_cpf)))

    def test_invalid_cpf(self):
        '''CPF must be invalid'''
        self.assertFalse(utils.validar_cpf('111.233.444-33'))

    def test_valid_cnpj(self):
        '''Check is CNPJ'''
        self.assertEqual(utils.validar_cnpj(self.valid_cnpj), ''.join(findall('\d+', self.valid_cnpj)))

    def test_invalid_cnpl(self):
        '''Check cnpj is invalid '''
        self.assertFalse(utils.validar_cnpj('111.222.333/0111-666'))

    def test_formt_cnpj(self):
        '''Test formating cnpj'''
        cnpj =  findall('\d+', self.valid_cnpj)
        cnpj = ''.join(cnpj)
        self.assertEqual(self.valid_cnpj, utils.formata_cpf_cnpj(cnpj))

    def test_formt_cpf(self):
        '''Test formating cpf '''
        cpf = findall('\d+', self.valid_cpf)
        cpf = ''.join(cpf)
        self.assertEqual(self.valid_cpf, utils.formata_cpf_cnpj(cpf))

    def test_is_not_cpf_or_cnpj(self):
        '''test if is not cpf or cnpj '''
        self.assertFalse(utils.is_cpf_or_cnpj('263225847'))

    def test_is_not_valid_cpf_or_cnpj(self):
        '''test if is not valid cpf or cnpj '''
        self.assertFalse(utils.valida_cpf_cnpj('263225847'))

    def test_is_not_valid_cnpj(self):
        '''test if is not cpf or cnpj '''
        self.assertFalse(utils.validar_cnpj('263225847'))

    def test_is_not_valid_cpf(self):
        '''test if is not cpf or cpf '''
        self.assertFalse(utils.validar_cpf('263225847'))

    def test_cnpj_or_cpf_valid_cnpj(self):
        '''Test if cnpj is valid on cpf_cpf '''
        self.assertEqual(utils.valida_cpf_cnpj(self.valid_cnpj), ''.join(findall('\d+', self.valid_cnpj)))

    def test_cnpj_or_cpf_valid_cpf(self):
        '''Test if cpf is valid on cpf_cpf '''
        self.assertEqual(utils.valida_cpf_cnpj(self.valid_cpf), ''.join(findall('\d+', self.valid_cpf)))