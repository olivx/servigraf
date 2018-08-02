from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.shortcuts import resolve_url
from django.test import TestCase
from django.contrib import auth
from model_mommy import mommy

from core.models import Cliente
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

        self.user.profile.type = Profile.CLIENT_USER
        self.user.profile.company = mommy.make(Cliente)
        self.user.save()
        self.user.profile.save()

    def test_if_profile_is_client(self):
        ''' test if profile is cliente '''
        user =  User.objects.first()
        self.assertEqual(Profile.CLIENT_USER, user.profile.type)

    def test_login_by_username_cliente(self):
        ''' Test login by usernmae if is CLIENT_USER'''
        data = {'username':'olvx', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data, follow=True)
        self.assertEqual(200, resp.status_code)

    def test_login_by_email_cliente_user(self):
        ''' Test login by usernmae if is CLIENT_USER'''
        data = {'username':'oliveira@email.com', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data, follow=True)
        self.assertEqual(200, resp.status_code)

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

class TestClientHasCompnay(TestCase):
    def setUp(self):
        self.user = mommy.make(User, is_active=True, username='olvx' ,email='oliveira@email.com')
        self.user.set_password(123)

        self.user.profile.company = None
        self.user.profile.type = Profile.CLIENT_USER
        self.user.save()
        self.user.profile.save()

    def test_user_is_anonymous(self):
        ''' Test user has company to login'''
        self.user.profile.save()
        data = {'username':'oliveira@email.com', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data)
        user = auth.get_user(resp.client)
        self.assertEqual(user.is_anonymous(),True)

    def test_user_is_anonymous_error_message(self):
        ''' Test user has company to login message error'''
        self.user.profile.save()
        data = {'username':'oliveira@email.com', 'password':123}
        resp = self.client.post(resolve_url('account:login'), data, follow=True)
        messages = resp.context['messages']
        _messages = list(get_messages(resp.wsgi_request))

        self.assertEqual(len(list(messages)), 1)
        self.assertEqual(str(_messages[0]), 'Usuário cliente não tem empresa associada.')
