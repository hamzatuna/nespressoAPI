from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.dates import MonthArchiveView,WeekArchiveView,DayArchiveView
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import *
from .forms import *
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
from .decorators import manager_required
from .permissions import IsManager, IsPersonnelorManager
import json
from django.core import serializers
from datetime import datetime,date,timedelta
from django.db import connection
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.http import *
from django.urls import reverse
from django.conf import settings
import urllib

def to_json(objects):
    return serializers.serialize('json', objects)

@api_view(['GET'])
@manager_required
def dashboard_main(request):
    try:
        context = {}
        context["daily_sales_count"] = Sales.objects.filter(date__year=date.today().year,
                                                      date__month=date.today().month,
                                                      date__day=date.today().day).count()
        context["weekly_sales_count"] = Sales.objects.filter(date__gte=datetime.now() - timedelta(days=7)).count()
        return render(request,'dashboard_main.html',context)
    except KeyError:
        return Response(KeyError)

@api_view(['GET','POST'])
@manager_required
def dashboard_add_location(request):
    try:
        if request.method == "GET":
            form_context = {}
            form_context["locations_form"] = LocationsForm()
            form_context["locations_form"].fields['name'].widget.attrs = {'class': 'form-control'}
            print(form_context)
            return render(request,'dashboard_add_location.html',form_context)
        elif request.method == "POST":
            locations_form = LocationsForm(request.POST)
            if locations_form.is_valid():
                location = locations_form.save()
                form_context = {}
                form_context["locations_form"] = LocationsForm()
                form_context["locations_form"].fields['name'].widget.attrs = {'class': 'form-control'}
                return render(request,'dashboard_add_location.html',form_context)
    except KeyError:
        return Response(KeyError)


@api_view(['GET','POST'])
@manager_required
def dashboard_add_machine(request):
    try:
        if request.method == "GET":
            form_context = {}
            form_context["machines_form"] = MachinesForm()
            return render(request,'dashboard_add_machine.html',form_context)
        elif request.method == "POST":
            machines_form = MachinesForm(request.POST)
            if machines_form.is_valid():
                machine = machines_form.save()
                form_context = {}
                form_context["machines_form"] = MachinesForm()
                return render(request,'dashboard_add_machine.html',form_context)
    except KeyError:
        return Response(KeyError)

'''
@api_view(['GET','POST'])
@manager_required
def dashboard_add_stock(request):
    try:
        if request.method == "GET":
            form_context = {}
            form_context["stock_form"] = StockForm()
            return render(request,'dashboard_add_stock.html',form_context)
        elif request.method == "POST":
            stock_form = StockForm(request.POST)
            #if stock_form.is_valid():
            print("BURA")
            #stock = stock_form.cleaned_data['stock']
            #name = stock_form.cleaned_data['name']
            #print(name,stock)
            form_context = {}
            form_context["stock_form"] = StockForm()
            return render(request,'dashboard_add_stock.html',form_context)
    except KeyError:
        return Response(KeyError)
'''
@api_view(['GET','POST'])
@manager_required
def dashboard_add_stock(request):
    try:
        if request.method == "GET":
            form_context = {}
            form_context["location_form"] = Locations.objects.values_list('id','name', named=True)
            return render(request,'dashboard_add_stock.html',form_context)
        elif request.method == "POST":
            form_location_id = request.POST.get('location_id')
            form_stock = request.POST.get('stock')
            Locations.objects.filter(id=form_location_id).update(stock=form_stock)
            form_context = {}
            form_context["location_form"] = Locations.objects.values_list('id','name', named=True)
            return render(request,'dashboard_add_stock.html',form_context)
    except KeyError:
        return Response(KeyError)

@api_view(['GET','POST'])
@manager_required
def dashboard_add_sales_target(request):
    try:
        if request.method == "GET":
            personnel_dict = {}
            personnel_dict["personnels"] = Personnels.objects.select_related('location')
            return render(request,'dashboard_add_sales_target.html',personnel_dict)
        elif request.method == "POST":
            form_location_id = request.POST.get('location_id')
            form_stock = request.POST.get('stock')
            Locations.objects.filter(id=form_location_id).update(stock=form_stock)
            form_context = {}
            form_context["sales_target_form"] = Personnels.objects.values_list('user_id', 'name', named=True)
            return render(request,'dashboard_add_sales_target.html',form_context)
    except KeyError:
        return Response(KeyError)



@api_view(['GET','POST'])
@manager_required
def dashboard_add_personnel(request):
    try:
        if request.method == "GET":
            form_context = {}
            form_context["personnels_form"] = PersonnelsForm()
            form_context["user_form"] = AutoUserForm()
            return render(request,'dashboard_add_personnel.html',form_context)
        elif request.method == "POST":
            personnels_form = PersonnelsForm(request.POST)
            user_form = AutoUserForm(request.POST)
            print(form_to_json(personnels_form))
            if personnels_form.is_valid() and user_form.is_valid():
                #personnel = personnels_form.save()
                '''
                user = User(**user_form)
                print(user)
                user.set_password(user_form['password'])
                user.user_type = 2
                user.save()
                Personnels.objects.create(user=user, **personnels_form)
                '''
                form_context = {}
                form_context["personnels_form"] = PersonnelsForm()
                form_context["user_form"] = AutoUserForm()
                return render(request,'dashboard_add_personnel.html',form_context)
    except KeyError:
        return Response(KeyError)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user_object = User.objects.get(id = token.user_id)
        return Response({'token': token.key, 'id': token.user_id, 'user_type':user_object.user_type})

@api_view(['GET','POST'])
def login_site(request):
    try:
        logout(request)
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if user.user_type == 1: #Dashboard'a sadece admin login olabilir.
                        login(request, user)
                        return HttpResponseRedirect(reverse('dashboard_main'))
                        '''
                        #Begin reCAPTCHA validation
                        recaptcha_response = request.POST.get('g-recaptcha-response')
                        url = 'https://www.google.com/recaptcha/api/siteverify'
                        values = {
                            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                            'response': recaptcha_response
                        }
                        data = urllib.parse.urlencode(values).encode()
                        req = urllib.request.Request(url, data=data)
                        response = urllib.request.urlopen(req)
                        result = json.loads(response.read().decode())
                        #End reCAPTCHA validation

                        if result['success']:
                            login(request, user)
                            return HttpResponseRedirect(reverse('dashboard_main'))
                        else:
                            login_context = {}
                            login_context["is_failed"] = 1
                            return render(request, 'login.html', login_context)
                        '''
            else:
                login_context = {}
                login_context["is_failed"] = 1
                return render(request, 'login.html', login_context)
        #return HttpResponseRedirect(reverse("login"))
        return render(request, 'login.html')
    except KeyError:
        return Response(KeyError)

@api_view(['GET'])
def logout_site(request):
    try:
        logout(request)
        return HttpResponseRedirect(reverse("login"))
    except:
        return Response(KeyError)



@api_view(['GET','POST'])
def get_filtered_sales(request):
    #print(request.data['personnel_name'])
    try:
        cursor = connection.cursor()
        print(request.POST)
        #query = '''select "SL"."CustomerName" from "Sales" as "SL" INNER JOIN "Personnels" as "PL" ON ("SL"."personnel_id" = "PL"."user_id")     INNER JOIN "Machines" as "MC" ON ("SL"."MachineId" = "MC"."id")    INNER JOIN "Locations" as "LC" ON ("SL"."location_id" = "LC"."id") '''
        #query = '''select "SL"."CustomerName","SL"."CustomerSurname","SL"."CustomerName","SL"."CustomerPhoneNumber","SL"."CustomerEmail","MC"."","LC"."name" from "Sales" as "SL" INNER JOIN "Personnels" as "PL" ON ("SL"."personnel_id" = "PL"."user_id")     INNER JOIN "Machines" as "MC" ON ("SL"."MachineId" = "MC"."id")    INNER JOIN "Locations" as "LC" ON ("SL"."location_id" = "LC"."id") '''
        query = '''select * from "Sales" as "SL" INNER JOIN "Personnels" as "PL" ON ("SL"."personnel_id" = "PL"."user_id") INNER JOIN "Machines" as "MC" ON ("SL"."MachineId" = "MC"."id")    INNER JOIN "Locations" as "LC" ON ("SL"."location_id" = "LC"."id") '''
        if request.method=='POST':
            if request.data['personnel_name'] and request.data['personnel_name'] is not None:
                personnel_name = request.data['personnel_name']
                condition = '''WHERE "PL"."name" = '{0}' '''.format(personnel_name)
                query = query+condition

            if request.data['personnel_surname'] and request.data['personnel_surname'] is not None:
                personnel_surname = request.data['personnel_surname']
                condition = '''WHERE "PL"."surname" = '{0}' '''.format(personnel_surname)
                query = query+condition

            if request.POST.get("filterObject[startdate]"):
                startdate = request.data['startdate']
                condition = '''WHERE "SL"."Date" > '{0}' '''.format(startdate)
                query = query+condition

            if request.data['enddate'] and request.data['enddate'] is not None:
                enddate = request.data['enddate']
                condition = '''WHERE "SL"."Date" < '{0}' '''.format(enddate)
                query = query+condition

            if request.data['machine_id'] and request.data['machine_id'] is not None:
                machine_id = request.data['machine_id']
                condition = '''WHERE "MC"."id" = '{0}' '''.format(machine_id)
                query = query+condition

            if request.data['is_campaign'] and request.data['is_campaign'] is not None:
                is_campaign = request.data['is_campaign']
                condition = '''WHERE "SL"."IsCampaign" = '{0}' '''.format(is_campaign)
                query = query+condition

            if request.data['location_id'] and request.data['location_id'] is not None:
                location_id = request.data['location_id']
                condition = '''WHERE "SL"."location_id" = '{0}' '''.format(location_id)
                query = query+condition

            print(query)
            cursor.execute(query)
            rows = cursor.fetchall()
            print(rows)
            return HttpResponse("",status=200)
    except Exception as e:
        print(e)
        return HttpResponse("",status=500)


@api_view(['GET'])
@manager_required
def get_sales_count(request):
    try:
        d = {}
        d["daily_sales_count"] = Sales.objects.filter(Date__year = date.today().year,
                                                 Date__month= date.today().month,
                                                 Date__day= date.today().day).count()

        #d["daily_sales_count"] = Sales.objects.filter(Date__startswith = datetime).count()

        d["weekly_sales_count"] = Sales.objects.filter(Date__gte = datetime.now()-timedelta(days=7)).count()
        #return HttpResponse(to_json(d), content_type='application/json', status=200)
        return HttpResponse(json.dumps(d),status=200)
    except KeyError:
        return Response(KeyError)



@api_view(['GET'])
def home(request):
    return render(request,'home.html')

class RegisterUser(CreateAPIView):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

class RegisterPersonnel(CreateAPIView):
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all()
    permission_classes = (IsManager,)

@api_view(['POST'])
def insert_sales(request):
    sales = Sales()
    serializer = SalesSerializer(sales,data=request.data)
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    except KeyError:
        return Response(KeyError)

class SalesListCreate(generics.ListCreateAPIView):
    serializer_class = SalesSerializer
    queryset = Sales.objects.all()
    permission_classes = (IsPersonnelorManager,)

class TastingInformationsList(generics.ListCreateAPIView):
    serializer_class = TastingInformationsSerializer
    queryset = TastingInformations.objects.all()

class PersonnelsListCreate(generics.ListCreateAPIView):
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all()
    permission_classes = (IsManager,)

class MachinesListCreate(generics.ListCreateAPIView):
    serializer_class = MachinesSerializer
    permission_classes = (IsPersonnelorManager,)
    queryset = Machines.objects.all()

class LocationsListCreate(generics.ListCreateAPIView):
    serializer_class = LocationsSerializer
    queryset = Locations.objects.all()
    permission_classes = (IsPersonnelorManager,)

class LocationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LocationsSerializer
    queryset = Locations.objects.all()
    permission_classes = (IsPersonnelorManager,)


class LocationListCreate(generics.ListCreateAPIView):
    serializer_class = LocationsSerializer
    queryset = Locations.objects.all()
    permission_classes = (IsPersonnelorManager,)

class CustomerGoalListCreate(generics.ListCreateAPIView):
    serializer_class = CustomerGoalSerializer
    queryset = CustomerGoals.objects.all()
    permission_classes = (IsPersonnelorManager,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data,list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CustomerGoalDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerGoalSerializer
    queryset = CustomerGoals.objects.all()
    permission_classes = (IsPersonnelorManager,)

class StockListCreate(generics.ListCreateAPIView):
    serializer_class = StockSerializer
    permission_classes = (IsPersonnelorManager,)

    def get_queryset(self):
        user = self.request.user

        # if user is manager return all Sales
        if user.user_type==1:
            return Stock.objects.all()

        personnel_location = user.personnels.location_id

        return Stock.objects.filter(location=personnel_location)