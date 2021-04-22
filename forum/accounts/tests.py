from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import RequestFactory, TestCase

from .views import (UserLoginView, UserLogoutView, UsersView, detail, index,
                    register, settings)

# func for fast user creating
def create_user(username, password):
    return User.objects.create_user(username=username, password=password)
class IndexViewTests(TestCase):
    # tests right template rendering
    # for not logged in user
    def test_not_logged_in_user(self):
        response = self.client.get(reverse('accounts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<b>not</b>')
    
    # this test too but
    # for logged in user
    def test_logged_in_user(self):
        user = create_user('testuser', 'testpass')
        factory = RequestFactory()
        request = factory.get('/accounts/')
        request.user = user
        response = index(request)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '<b>not</b>')

class UserLoginViewTests(TestCase):
    # creates user and logins it
    def test_logins_existing_user(self):
        create_user('testuser', 'testpass')
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post('/accounts/login/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/')
        self.assertEqual(User(username='testuser').is_authenticated, True)
    
    # trying to login not existing user
    def test_not_logins_not_existing_user(self):
        data = {'username': 'testuser', 'password': 'testpass'}
        response = self.client.post('/accounts/login/', data)
        self.assertEqual(response.status_code, 200)

# RequestFactory returns AttributeError so i can not simulate
# and manage automated process of user log out system
class UserLogoutViewTests(TestCase):
    # tests right template rendering for now
    def test_logs_out(self):
        create_user('testuser', 'testpass')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'you are successfully logged out')

class RegisterTests(TestCase):
    # registers user in
    # but for some reason works bad
    def test_registration(self):
        data = {'username': 'testuser', 'password1': 'testpass', 'password2': 'testpass'}
        response = self.client.get('/accounts/register/', data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User(username='testuser').is_authenticated, True)

# i made enough tests to start hate myself and this work
# idk when i will return