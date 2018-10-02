import logging
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import (
        User,
        Personnels,
)


class RegisterUserTestCases(APITestCase):
    url = '/register'

    def setUp(self):
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
    personnel_data = {
        "user": {
            "username": "test-user-name4",
            "password": "12345678.",
            "email": "a4@a.com",
            "is_active": True,
            "user_type": 1
        },
        
        "name": "test-name",
        "surname": "test-surname",
        "email": "a1@a.com"
    }

    def setUp(self):
        User.objects.all().delete()
        Personnels.objects.all().delete()
        Token.objects.all().delete()
        
        # add test user
        test_user_data = {
            "username": "test-user",
            "password": "12345678.",
            "email": "a5@a.com",
            "is_active": True,
            "user_type": 1
        }

        test_user = User(**test_user_data)
        test_user.save()
        
        self.token,_ = Token.objects.get_or_create(user=test_user)

        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_register_success(self):
        response = self.client.post(self.url, self.personnel_data, format='json')

        # get all personnels
        personnels = Personnels.objects.all()

    
        # expect to status code ok
        self.assertEqual(201, response.status_code)

        # expect personel is added successfully
        self.assertEqual(1, len(personnels))