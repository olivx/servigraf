from django.test import TestCase
from model_mommy import mommy
from django.contrib.auth.models import User

from account.models import Profile
# Create your tests here.
class TestModelProfile(TestCase):

    def setUp(self):
        self.user = mommy.make(User, first_name='thiago', last_name='oliveira')

    def test_create_profile(self):
        ''' test if exists Profile '''
        self.assertEqual(1, Profile.objects.count())

    def test_profile_full_name(self):
        ''' teste if full name is thiago oliveira '''
        self.assertEqual(self.user.get_full_name() , self.user.profile.full_name)

    def test_kind(self):
        ''' test if kind default user is normal user '''
        self.assertEqual(self.user.profile.type, Profile.NORMAL_USER)

    def test_birdayth_can_be_none(self):
        ''' test if date birdayth is None'''
        self.assertIsNone(self.user.profile.birdayth)
