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
from django.db.models.functions import Cast
from django.db.models import CharField
import urllib
from . import sale_filters
from django.forms.models import model_to_dict
import xlwt

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

@api_view(['GET', 'POST'])
def login_site(request):
    try:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    if user.user_type == 1: #Dashboard'a sadece admin login olabilir.
                        login(request, user)
                        return HttpResponseRedirect(reverse('dashboard_main'))
            else:
                login_context = {}
                login_context["is_failed"] = 1
                return render(request, 'login.html', login_context)
        
        elif request.method=='GET' and request.user.is_authenticated:
            return HttpResponseRedirect(reverse('dashboard_main'))
        
        else:
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

@api_view(['PUT', 'PATCH'])
def update_personnel(request, pk):
    try:
        instance = Personnels.objects.get(user_id=pk)
        validated_data = request.data

        # updatelenebilir fieldlar
        updated_keys = [
            "name",
            "surname",
            "phone_number",
            "tc_no"
        ]

        # update personnel fields
        for field in updated_keys:
            updated_value = validated_data.pop(field, getattr(instance, field))
            setattr(instance, field, updated_value)

        # check email changed
        if 'email' in validated_data['user']:
            instance.user.email = validated_data['user']['email']
            instance.user.save()

        # lokasyonu degistir
        instance.location_id = validated_data['location']['id']

        instance.save()

        return Response({'status': 'ok'}, status=200)

    except Personnels.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

class RegisterUser(CreateAPIView):
    serializer_class = UsersSerializer
    queryset = User.objects.all()

class RegisterPersonnel(CreateAPIView):
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all()
    permission_classes = (IsManager,)

class UpdatePersonnelView(generics.UpdateAPIView):
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all()
    permission_classes = (IsManager,)

class PersonnelDetailView(generics.RetrieveAPIView):
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all()
    permission_classes = (IsManager,)

class SaleDetailView(generics.RetrieveAPIView):
    serializer_class = SalesSerializer
    queryset = Sales.objects.all()
    permission_classes = (IsManager,)

class FilterSalesView(generics.ListAPIView):
    serializer_class = SalesSerializer

    def get_queryset(self):
        data = self.request.data
        filters = sale_filters.get_sale_filters(data)

        return Sales.objects.filter(*filters)

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

@api_view(['POST'])
def filter_sales(request):
    """
    keyler:
        startdate: baslangic zamani  -- eklenmedigi durumlar: (None, 'null')
        enddate: bitis zamani  -- eklenmedigi durumlar: (None, 'null')
        location_id: bu lokasyondaki satislar -- eklenmedigi durumlar: (None, '')
        personnel_name: personel adi -- eklenmedigi durumlar: (None, '')
        personel_surname: personel soyadi -- eklenmedigi durumlar: (None, 'null')
        is_campaign: is_campaign {'1', '0'} -- eklenmedigi durumlar {None, ''}
        machine_id: bu makineden satislar {string olabilir}
    """

    # get json data
    data = request.data

    filters = sale_filters.get_sale_filters(data)
    queryset = Sales.objects.filter(*filters)

    serializer = SalesSerializer(queryset, many=True)
    
    return Response({"data":serializer.data})


@api_view(['POST'])
def export_sales(request):
    """
    keyler:
        startdate: baslangic zamani  -- eklenmedigi durumlar: (None, 'null')
        enddate: bitis zamani  -- eklenmedigi durumlar: (None, 'null')
        location_id: bu lokasyondaki satislar -- eklenmedigi durumlar: (None, '')
        personnel_name: personel adi -- eklenmedigi durumlar: (None, '')
        personel_surname: personel soyadi -- eklenmedigi durumlar: (None, 'null')
        is_campaign: is_campaign {'1', '0'} -- eklenmedigi durumlar {None, ''}
        machine_id: bu makineden satislar {string olabilir}
    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sales.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sale')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = [
        'Tarih', 
        'Lokasyon', 
        'Satis Elemani Adi',
        'Satis Elemani Soy Adi',
        'Makine',
        'Musteri Adi',
        'Musteri Soy Adi',
        'Musteri tel',
        'Musteri Email',
        'Kampanyali'
    ]
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    # get json data
    #data = request.data if request.POST else {}
    if request.method == "POST":
        print("İSTEĞİMİZ POST")
        data = request.data
    #print("İŞTEE O VERİ  ",data)
    #data = {}
    filters = sale_filters.get_sale_filters(data)

    objects = Sales.objects.filter(*filters).annotate(formatted_date=Cast('date', CharField()))
    rows = objects.values_list(
        'formatted_date',
        'location__name',
        'personnel__name',
        'personnel__surname',
        'machine__name',
        'customer_name',
        'customer_surname',
        'customer_phone_number',
        'customer_email',
        'is_campaign'
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

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


def validate_token(request):
    if request.user.is_authenticated:
        return Response({"status":"ok"})
    else:
        return Response({"status":"INVALID"})