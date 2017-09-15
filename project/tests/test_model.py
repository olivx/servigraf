from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from core.models import Cliente
from catalogo.models import Produto
from project.models import Projects, ProjectServices


# Create your tests here.



class TestModelProject(TestCase):
    def login_user(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')

    def setUp(self):
        self.login_user()
        self.cliente_1 = mommy.make(Cliente, nome_fantasia='Cliente 1')
        self.cliente_2 = mommy.make(Cliente, nome_fantasia='Cliente 2')
        self.project = mommy.make(Projects, name='project name')
        self.project.clients.add(self.cliente_1)
        self.project.clients.add(self.cliente_2)

    def test_create(self):
        """test count must have 1 project """
        self.assertEqual(Projects.objects.count(), 1)

    def test_str(self):
        """test str must be project name """
        self.assertEqual('project name', self.project.__str__())

    def test_has_client(self):
        """Cliente Project must have a client and project"""
        with self.subTest():
            self.assertIsInstance(self.project.clients.first(), Cliente)

    def test_project_has_more_one_client(self):
        """Porject can have more than one client"""
        with self.subTest():
            self.assertEqual(1, Projects.objects.filter(pk=self.project.id).count())
            self.assertEqual(2, Projects.objects.get(pk=self.project.id).clients.count())

    def test_get_absolute_url(self):
        """test absolue url """
        resp = self.client.get(self.project.get_absolute_url())
        self.assertEqual(200, resp.status_code)


class TestProjectServico(TestCase):

    def login_user(self):
        user = User.objects.create(username='olvx', email='oliveravicente.net@gmial.com')
        user.set_password('logan277')
        user.save()
        self.client.login(username='olvx', password='logan277')

    def setUp(self):
        self.project = mommy.make(Projects, name='Projeto teste')
        self.service = mommy.make(Produto, nome='Produto teste')
        self.project_services = mommy.make(ProjectServices, _quantity=5)
        self.project_service = mommy.make(ProjectServices, project=self.project, service=self.service, valor=25.96)


    def test_str(self):
        _str = '%s | %s' % (self.project_service.service.nome, self.project_service.valor)
        self.assertEqual(_str, self.project_service.__str__())


    