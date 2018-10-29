import logging
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import (
        User,
        Personnels,
        Locations,
        Sales,
        Machines,
        Stock,
        StockHistory
)

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
        "email": "a1@a.com",
        "tc_no": 12345678901
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
    }

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Locations.objects.all().delete()

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

        # expect to status code ok
        self.assertEqual(201, response.status_code)

        # expect location is added successfully
        self.assertEqual(1, len(locations))

        # check field are correct
        location = locations[0].__dict__
        for key in self.location_data:
            self.assertEqual(location[key], self.location_data[key])


class SalesTestCases(APITestCase):
    
    personnel_id = 40
    machine_id = 40
    sales_data = {
            "PersonnelId": personnel_id,
            "CustomerName": "testName",
            "CustomerSurname": "CustomerSurname",
            "CustomerPhoneNumber": "23233232323",
            "CustomerEmail": "aawdaw@a.com",
            "Latitude": 45.1,
            "Longitude": 45.2,
            "Price": "23.000",
            "SerialNumber": "aweawe",
            "IsCampaign": True,
            "MachineId": machine_id,

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
            'id': self.machine_id,
            'Name': 'test_name',
        }
        test_machine = Machines(**test_machine_data)
        test_machine.save()

        # add location
        location_data = {
                "id": 20,
                "Latitude": 45.1,
                "Longitude": 34.12,
                "LocationName": "testPlace",
        }
        location = Locations(**location_data)
        location.save()

        # add personnel
        test_personnel_data = {
            "user": test_user,
            "name": "test-name",
            "surname": "test-surname",
            "location_id": location,
            "tc_no": 12345678901
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

class StockTestCases(APITestCase):
    
    user_id = 40
    machine_id = 40
    location_id = 40
    stock_data = {
        "id": 4,
        "stock_count": 5,
        "machine": machine_id,
        "location": location_id
    }
    url = '/stocks'

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Machines.objects.all().delete()
        Locations.objects.all().delete()
        
        # add test user
        test_user_data = {
            "id": self.user_id,
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
            'id': self.machine_id,
            'Name': 'test_name',
        }
        test_machine = Machines(**test_machine_data)
        test_machine.save()

        # add location
        location_data = {
                "id": self.location_id,
                "Latitude": 45.1,
                "Longitude": 34.12,
                "LocationName": "testPlace",
        }
        location = Locations(**location_data)
        location.save()

        # add personnel
        test_personnel_data = {
            "user": test_user,
            "name": "test-name",
            "surname": "test-surname",
            "location_id": location,
            "tc_no": 12345678901
        }
        test_personnel = Personnels(**test_personnel_data)
        test_personnel.save()
  
        self.token,_ = Token.objects.get_or_create(user=test_user)

        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_add_stock(self):

        response = self.client.post(self.url, self.stock_data, format='json')

        # get all stocks
        stocks = Stock.objects.all()
        stockHistories = StockHistory.objects.all()

        # expect to status code ok
        self.assertEqual(201, response.status_code)

        # expect stock is added successfully
        self.assertEqual(1, len(stocks))
        self.assertEqual(1, len(stockHistories))
