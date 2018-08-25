from django.urls import path, re_path,include
from rest_framework import generics
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('get_sales',views.get_sales,name="get_sales"),
    path('insert_sales', views.insert_sales, name="insert_sales"),
    path('insert_tastinginfo',views.TastingInformationsList.as_view(),name='tasting_list'),
    path('admin_get_sales',views.get_sales, name="get_sales"),
    path('users/register/', views.register_user, name="register"),
    #path('insert_machines', views.machines, name="insert_machines"),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('get-token', obtain_auth_token),

    path('home',views.home,name="home"),
    #path('admin_get_sales',views.SalesViewSet.as_view({'get': 'list'}),name="admin_get_sales")
]

