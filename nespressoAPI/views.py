from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from .serializers import SalesSerializer,MachinesSerializer
from .models import Managers,Locations,Personnels,Machines,Supervisors,Sales
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics
from rest_framework.exceptions import ValidationError

@api_view(['GET'])
def get_sales(request):
    sales = Sales.objects.all()
    serializer = SalesSerializer(sales,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def insert_sales(request):
    sales = Sales()
    serializer = SalesSerializer(Sales,data=request.data)
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    except KeyError:
        return Response(KeyError)



# @api_view(['GET','POST'])
# def machines(request):
#     if request.method=='GET':
#         machines = Machines.objects.all()
#         serializer = MachinesSerializer(machines,many=True)
#         return Response(serializer.data)
#     elif request.method=='POST':
#         try:
#             machines = Machines()
#             serializer = MachinesSerializer(machines, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 return Response(serializer.errors)
#         except KeyError:
#             return Response(KeyError)