import logging
import json
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
    location_id = 20
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
        "tc_no": 12345678901,
        "location_id": location_id
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
        
        # add location
        location_data = {
                "id": self.location_id,
                "latitude": 45.1,
                "longitude": 34.12,
                "name": "testPlace",
        }
        location = Locations(**location_data)
        location.save()
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
            "latitude": 45.1,
            "longitude": 34.12,
            "name": "testPlace",
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
    
    personnel = 40
    machine = 40
    location = 20
    initial_stock_count = 4
    sales_data = {
            "customer_name": "testName",
            "customer_surname": "customer_surname",
            "customer_phone_number": "23233232323",
            "customer_email": "aawdaw@a.com",
            "latitude": 45.1,
            "longitude": 45.2,
            "price": "23.000",
            "serial_number": "aweawe",
            "is_campaign": True,
            "machine": machine,
            "personnel": personnel,
    }
    url = '/sales'

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Personnels.objects.all().delete()
        Sales.objects.all().delete()
        Stock.objects.all().delete()
        # add test user
        test_user_data = {
            "id": self.personnel,
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
            'id': self.machine,
            'name': 'test_name',
        }
        test_machine = Machines(**test_machine_data)
        test_machine.save()

        # add location
        location_data = {
                "id": self.location,
                "latitude": 45.1,
                "longitude": 34.12,
                "name": "testPlace",
        }
        location = Locations(**location_data)
        location.save()

        # add personnel
        test_personnel_data = {
            "user": test_user,
            "name": "test-name",
            "surname": "test-surname",
            "location": location,
            "tc_no": 12345678901
        }
        test_personnel = Personnels(**test_personnel_data)
        test_personnel.save()

        # add stock
        test_stock_data = {
            'machine': test_machine,
            'location': location,
            'stock_count': self.initial_stock_count,
            'user': test_user
        }
        test_stock = Stock(**test_stock_data)
        test_stock.save()


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

        stock = Stock.objects.get(location=self.location, machine=self.machine)

        self.assertEqual(self.initial_stock_count-1, stock.stock_count)

class StockTestCases(APITestCase):
    
    user = 40
    machine = 40
    location = 40
    stock_data = {
        "id": 4,
        "stock_count": 5,
        "machine_id": machine,
        "location": location
    }
    url = '/stocks'

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Machines.objects.all().delete()
        Locations.objects.all().delete()
        
        # add test user
        test_user_data = {
            "id": self.user,
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
            'id': self.machine,
            'name': 'test_name',
        }
        test_machine = Machines(**test_machine_data)
        test_machine.save()

        # add location
        location_data = {
                "id": self.location,
                "latitude": 45.1,
                "longitude": 34.12,
                "name": "testPlace",
        }
        location = Locations(**location_data)
        location.save()

        # add personnel
        test_personnel_data = {
            "user": test_user,
            "name": "test-name",
            "surname": "test-surname",
            "location": location,
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

class SalesFilterTestCases(APITestCase):
    
    user = 40
    machine = 40
    location = 40

    url = '/filter/sales'
    filter_object = {
        'startdate': '2016-10-31T21:00:00.000Z', 
        'enddate': '2019-10-31T21:00:00.000Z', 
        'machine_id': machine, 
        'location_id': location,
        'personnel_name': 'test', 
        'personnel_surname': 'test', 
        'is_campaign': '1'
    }
    

    def setUp(self):
        User.objects.all().delete()
        Token.objects.all().delete()
        Sales.objects.all().delete()
        Machines.objects.all().delete()
        Locations.objects.all().delete()
        
        # add test user
        test_user_data = {
            "id": self.user,
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
            'id': self.machine,
            'name': 'test_name',
        }
        test_machine = Machines(**test_machine_data)
        test_machine.save()

        # add location
        location_data = {
                "id": self.location,
                "latitude": 45.1,
                "longitude": 34.12,
                "name": "testPlace",
        }
        location = Locations(**location_data)
        location.save()

        # add personnel
        test_personnel_data = {
            "user": test_user,
            "name": "test-name",
            "surname": "test-surname",
            "location": location,
            "tc_no": 12345678901
        }
        test_personnel = Personnels(**test_personnel_data)
        test_personnel.save()

        # add sale 
        sale_data = {
            "date": "2018-11-04T19:57:37.431053Z",
            "customer_name": "testName",
            "customer_surname": "CustomerSurname",
            "customer_phone_number": "23233232323",
            "customer_email": "aawdaw@a.com",
            "is_campaign": True,
            "latitude": 45.1,
            "longitude": 45.2,
            "price": "23.000",
            "serial_number": "aweawe",
            "machine": test_machine,
            "personnel": test_personnel,
            "location": location
        }
        sale = Sales(**sale_data)
        sale.save()

        self.token,_ = Token.objects.get_or_create(user=test_user)

        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_sale_filter_success(self):

        response = self.client.post(self.url, self.filter_object, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_sale_filter_success_null(self):

        response = self.client.post(self.url, {}, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 1)

    def test_sale_filter_machine_fail(self):
        filter_object_machine_fail = {**self.filter_object, "machine_id": 1}
        response = self.client.post(self.url, filter_object_machine_fail, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_sale_filter_location_fail(self):
        filter_object_location_fail = {**self.filter_object, "location_id": 1}
        response = self.client.post(self.url, filter_object_location_fail, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_sale_filter_startdate_fail(self):
        filter_object_fail = {**self.filter_object, "startdate": '2070-10-31T21:00:00.000Z'}
        response = self.client.post(self.url, filter_object_fail, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_sale_filter_enddate_fail(self):
        filter_object_fail = {**self.filter_object, "enddate": '2000-10-31T21:00:00.000Z'}
        response = self.client.post(self.url, filter_object_fail, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_sale_filter_is_campaign_fail(self):
        filter_object_fail = {**self.filter_object, "is_campaign": False}
        response = self.client.post(self.url, filter_object_fail, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_sale_filter_personnel_name_fail(self):
        filter_object_fail = {**self.filter_object, "personnel_name": 'ddddddd'}
        response = self.client.post(self.url, filter_object_fail, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 0)

    def test_sale_filter_personnel_surname_fail(self):
        filter_object_fail = {**self.filter_object, "personnel_surname": 'ddddddd'}
        response = self.client.post(self.url, filter_object_fail, format='json')

        # expect to status code ok
        self.assertEqual(200, response.status_code)

        # check object is pass all filters
        self.assertEqual(len(json.loads(response.content)), 0)