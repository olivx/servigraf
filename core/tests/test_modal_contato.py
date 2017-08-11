from django.core.exceptions import ValidationError
from django.test import TestCase
from model_mommy import mommy

from core.models import Contato, Telefone


class TestModelContact(TestCase):
    def setUp(self):
        self.contact = mommy.make(Contato)

    def test_contact_ativo(self):
        """Contact be default is ativo True"""
        self.assertTrue(self.contact.ativo)

    def test_str_contact(self):
        """Contact must be nome e sobre_none at str """
        self.assertEqual(str(self.contact), ' '.join([self.contact.nome, self.contact.sobre_nome]))


    def test_contact_name_cant_be_null_or_blank(self):
        """Contact must be a name """
        field =  Contato._meta.get_field('nome')
        self.assertFalse(field.null)
        self.assertFalse(field.blank)

    def test_contact_sobre_name_cant_be_blank_or_null(self):
        """ Contact must be a sobre_nome"""
        field = Contato._meta.get_field('sobre_nome')
        self.assertFalse(field.blank)
        self.assertFalse(field.null)

    def test_contact_observacao_cant_be_blank(self):
        """Contact observacao can be null or blank"""
        field = Contato._meta.get_field('observacao')
        self.assertTrue(field.blank)

class TestModelContatoTelefone(TestCase):

        def setUp(self):
            self.contact = mommy.make(Contato)
            self.contact.telefones.create(telefone='011970513508')


        def test_create_phone(self):
            """Test create telefone"""
            self.assertTrue(self.contact.telefones.exists())

        def test_phone_type_default(self):
            """ test type default is FIXO"""
            self.assertEqual(self.contact.telefones.first().tipo, Telefone.FIXO)

        def test_phone_is_numeric(self):
            for char in self.contact.telefones.first().telefone:
                self.assertTrue(char.isdigit())








