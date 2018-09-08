import logging
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User


class RegisterUserTestCases(APITestCase):
    url = '/register'

    def set_up(self):
        User.objects.all().delete()

    def test_register_success(self):
        response = self.client.post(self.url, {
            'username': 'testUser',
            'email': 'test@test.com',
            'password': 'test.test',
            'user_type': 1
        })

        # get all users
        users = User.objects.all()

        # expect to status code ok
        self.assertEqual(201, response.status_code)

        # expect user is added successfully
        self.assertEqual(1, len(users))
        
        # check data is 
        self.assertEqual(users[0].username, 'testUser')

class RegisterPersonnelTestCases(APITestCase):
    url = '/register/personnel'