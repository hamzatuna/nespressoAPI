import logging
from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class RegisterUserTestCases(TestCase):
    url = '/users/register/'

    def set_up(self):
        User.objects.all().delete()

    def test_register_success(self):
        response = self.client.post(self.url, {
            'username': 'testUser',
            'email': 'test@test.com',
            'password': 'test.test',
        })

        # get all users
        users = User.objects.all()

        # expect to status code ok
        self.assertEqual(201, response.status_code)

        # expect user is added successfully
        self.assertEqual(1, len(users))