from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from .serializers import (
    SalesSerializer,
    MachinesSerializer, 
    TastingInformationsSerializer,
    UserSerializer)
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
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import (
    Managers,
    Locations,
    Personnels,
    Machines,
    Supervisors,
    Sales,
    TastingInformations,
    IntensiveHours,
    MachineConditions,
    User)

@api_view(['GET'])
def home(request):
    return render(request,'home.html')

# class SalesViewSet(viewsets.ModelViewSet):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer

##############
# @api_view(['POST'])
# @permission_classes((permissions.AllowAny, ))
# def register_user(request):
#     newuser = request.data
#     serializer = UserSerializer(data=newuser)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUser(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


@api_view(['GET'])
def get_sales(request):
    sales = Sales.objects.all()
    serializer = SalesSerializer(sales,many=True)
    return Response(serializer.data)

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


class TastingInformationsList(generics.ListCreateAPIView):
    queryset = TastingInformations.objects.all()
    serializer_class = TastingInformationsSerializer



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