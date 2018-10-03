from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.dates import MonthArchiveView,WeekArchiveView,DayArchiveView
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from .serializers import *
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import *
import json
from django.core import serializers
from datetime import datetime,date,timedelta

def to_json(objects):
    return serializers.serialize('json', objects)

@api_view(['GET'])
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

    #weekly_sales_count =


@api_view(['GET'])
def home(request):
    return render(request,'home.html')

class RegisterUser(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class RegisterPersonnel(CreateAPIView):
    serializer_class = PersonnelSerializer
    queryset = Personnels.objects.all()

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

class TastingInformationsList(generics.ListCreateAPIView):
    serializer_class = TastingInformationsSerializer
    queryset = TastingInformations.objects.all()

class PersonnelsListCreate(generics.ListCreateAPIView):
    serializer_class = PersonnelsSerializer
    queryset = Personnels.objects.all()