from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy
from django.shortcuts import resolve_url as r
from django.forms import model_to_dict
import json

from core.models import Contato, Cliente


class TesTContatoSave(TestCase):
    def setUp(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')

        self.cli = mommy.make(Cliente, nome_fantasia='cliente LTDA')
        self.contato = mommy.make(Contato, nome='thiago')
        self.data = model_to_dict(self.contato, fields=[field.name for field in self.contato._meta.fields])
        self.resp_get = self.client.get(r('servigraf:contact_save', self.cli.id))
        self.resp_post = self.client.get(r('servigraf:contact_save', self.cli.id), self.data)
        self.resp_json = json.loads(self.resp_post.content.decode('utf-8'))

    def test_contato_save_get(self):
        """contact get  statu_code """
        self.assertEqual(200, self.resp_get.status_code)

    def test_contato_save_post(self):
        """contact post form valid  """
        self.assertTrue(self.resp_json['is_form_valid'])
