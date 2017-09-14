from django.test import TestCase
from model_mommy import mommy
from project.models import Projects


# Create your tests here.

class TestModelProject(TestCase):
    def test_create(self):
        mommy.make(Projects, name='project name')
        self.assertEqual(Projects.objects.count(), 1)
