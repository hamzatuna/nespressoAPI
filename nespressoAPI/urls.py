from django.urls import path, re_path,include
from rest_framework import generics
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView


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
    path('dashboard',TemplateView.as_view(template_name='dashboard_main.html'),name="dashboard_main"),
    path('dashboard_sales_tab',TemplateView.as_view(template_name='dashboard_sales_tab.html'),name="dashboard_sales_tab"),
    path('dashboard_tasting_tab',TemplateView.as_view(template_name='dashboard_tasting_tab.html'),name="dashboard_tasting_tab")
]

