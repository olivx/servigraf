from django.test import TestCase
from model_mommy import mommy
from django.contrib.auth.models import User

from django.shortcuts import resolve_url
from account.views import login

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



class TestViewsLogin(TestCase):
    def setUp(self):
        self.user = mommy.make(User, is_active=True, username='olvx' ,email='oliveira@email.com')
        self.user.set_password(123)

        self.user.profile.type = Profile.ESCOLA_DA_VILLA_USER
        self.user.save()
        self.user.profile.save()

    def test_if_profile_is_valla(self):
        ''' test if profile is villa scholl'''
        user =  User.objects.first()
        self.assertEqual(Profile.ESCOLA_DA_VILLA_USER, user.profile.type)

    def test_login_by_username_villa_user(self):
        ''' Test login by usernmae if is ESCOLA_DA_VILLA_USER'''
        data = {'username':'olvx', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data)
        self.assertEqual(302, resp.status_code)

    def test_login_by_email_villa_user(self):
        ''' Test login by usernmae if is ESCOLA_DA_VILLA_USER'''
        data = {'username':'oliveira@email.com', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data)
        self.assertEqual(302, resp.status_code)

    def test_login_by_username_normal_user(self):
        ''' Test login by usernmae if is NORMAL_USER'''
        self.user.profile.type = Profile.NORMAL_USER
        self.user.profile.save()
        data = {'username':'olvx', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data)
        self.assertEqual(302, resp.status_code)

    def test_login_by_email_normal_user(self):
        ''' Test login by usernmae if is NORMAL_USER'''
        self.user.profile.type = Profile.NORMAL_USER
        self.user.profile.save()
        data = {'username':'oliveira@email.com', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data)
        self.assertEqual(302, resp.status_code)
