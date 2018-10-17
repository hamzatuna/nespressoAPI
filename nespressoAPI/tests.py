import logging
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import (
        User,
        Personnels,
        Locations,
        LocationHistory,
        Sales,
        Machines
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

class LocationTestCases(APITestCase):
    url = '/locations/'
    location_data = {
            "Latitude": 45.1,
            "Longitude": 34.12,
            "LocationName": "testPlace",
            "stock": 2
    }

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Locations.objects.all().delete()
        LocationHistory.objects.all().delete()

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
    
    def test_add_location(self):
        response = self.client.post(self.url, self.location_data, format='json')

        # get all personnels
        locations = Locations.objects.all()
        location_histories = LocationHistory.objects.all()

        # expect to status code ok
        self.assertEqual(201, response.status_code)

        # expect location is added successfully
        self.assertEqual(1, len(locations))

        # check field are correct
        location = locations[0].__dict__
        for key in self.location_data:
            self.assertEqual(location[key], self.location_data[key])

        # check location is logged
        self.assertEqual(1, len(location_histories))

        self.assertEqual(location_histories[0].stock, self.location_data["stock"])
    
class LocationUpdateTestCases(APITestCase):
    location_data = {
            "id": 20,
            "Latitude": 45.1,
            "Longitude": 34.12,
            "LocationName": "testPlace",
            "stock": 2
    }
    url = '/locations/{}/'.format(location_data['id'])

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Locations.objects.all().delete()
        LocationHistory.objects.all().delete()

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
        location = Locations(**self.location_data)
        location.save()
        
        self.token,_ = Token.objects.get_or_create(user=test_user)

        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_update_location(self):
        updated_data = {
            **self.location_data,
            'stock': 45}
        response = self.client.put(self.url, updated_data, format='json')

        # get all personnels
        locations = Locations.objects.all()
        location_histories = LocationHistory.objects.all()

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # expect location is added successfully
        self.assertEqual(1, len(locations))

        # check field are correct
        location = locations[0].__dict__
        for key in updated_data:
            self.assertEqual(location[key], updated_data[key])

        # check location is logged
        self.assertEqual(2, len(location_histories))

        self.assertEqual(location_histories[1].stock, updated_data["stock"])

class SalesTestCases(APITestCase):
    
    personnel_id = 40
    initial_stock = 2
    sales_data = {
            "PersonnelId": personnel_id,
            "CustomerName": "testName",
            "CustomerSurname": "CustomerSurname",
            "CustomerPhoneNumber": "23233232323",
            "CustomerEmail": "aawdaw@a.com",
            "IsCampaign": True
    }
    url = '/sales'

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Personnels.objects.all().delete()
        Sales.objects.all().delete()

        # add test user
        test_user_data = {
            "id": self.personnel_id,
            "username": "test-user",
            "password": "12345678.",
            "email": "a5@a.com",
            "is_active": True,
            "user_type": 2
        }
        test_user = User(**test_user_data)
        test_user.save()


        # add machine
        test_machine_data = {
            'Name': 'test_name',
            'SerialNumber': '1234',
            'Fee': 2121
        }
        test_machine = Machines(**test_machine_data)
        test_machine.save()

        # add location
        location_data = {
                "id": 20,
                "Latitude": 45.1,
                "Longitude": 34.12,
                "LocationName": "testPlace",
                "stock": self.initial_stock,
                'machine': test_machine
        }
        location = Locations(**location_data)
        location.save()

        # add personnel
        test_personnel_data = {
            "user": test_user,
            "name": "test-name",
            "surname": "test-surname",
            "location_id": location
        }
        test_personnel = Personnels(**test_personnel_data)
        test_personnel.save()
  
        self.token,_ = Token.objects.get_or_create(user=test_user)

        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_add_sale(self):

        response = self.client.post(self.url, self.sales_data, format='json')

        # get all personnels
        sales = Sales.objects.all()

        # expect to status code ok
        self.assertEqual(201, response.status_code)

        # expect location is added successfully
        self.assertEqual(1, len(sales))

        # check stock is decreased
        self.assertEqual(sales[0].LocationId.stock, self.initial_stock-1)
        
