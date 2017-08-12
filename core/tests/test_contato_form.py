from django.test import TestCase
from core.forms import ContactForm

class TestContatoForm(TestCase):

    def test_form_has_field(self):
        """form must be 4 field """
        form = ContactForm()
        expect = ['nome', 'sobre_nome', 'observacao']
        self.assertSequenceEqual(expect, list(form.fields))

    def test_has_name(self):
        """form must he  nome """
        form = self.make_valid(nome='')
        self.assertTrue(form.errors)

    def test_has_sobre_nome(self):
        """form must have sobre nome"""
        form = self.make_valid(sobre_nome='')
        self.assertTrue(form.errors)

    def test_is_valid(self):
        """form must be valid"""
        self.assertFalse(self.make_valid().errors)

    def make_valid(self, **kwargs):
        valid = dict(nome='thiago', sobre_nome='oliveira',
            obeservacao='teste formulario')
        data = dict(valid, **kwargs)
        form = ContactForm(data)
        form.is_valid()
        return form