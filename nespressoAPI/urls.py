from django.urls import path, re_path,include
from rest_framework import generics
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView


urlpatterns = [
    path('get_sales', views.get_sales,name="get_sales"),
    path('register', views.RegisterUser.as_view()),
    path('register/personnel', views.RegisterPersonnel.as_view()),
    path('insert_sales', views.insert_sales, name="insert_sales"),
    path(
        'insert_tastinginfo',
        views.TastingInformationsList.as_view(),
        name='tasting_list'
    ),
    path('admin_get_sales', views.get_sales, name="get_sales"),
    # path('users/register/', views.register_user, name="register"),
    #path('get_sales',views.get_sales,name="get_sales"),
    #path('insert_sales', views.insert_sales, name="insert_sales"),
    path('get_sales',views.SalesListCreate.as_view(), name="sales_list"),
    path('insert_sales', views.SalesListCreate.as_view(), name="sales_create"),
    path('insert_tastinginfo',views.TastingInformationsList.as_view(),name='tasting_list'),

    path('admin_get_sales',views.SalesListCreate.as_view(), name="get_sales"),
    path('admin_get_tasting_informations',views.TastingInformationsList.as_view(),name='tasting_list'),

    path('get_sales_count',views.get_sales_count,name="get_sales_count"),

    path('get_personnels',views.PersonnelsListCreate.as_view(),name="get_personnels"),
    path('users/register/', views.register_user, name="register"),
    #path('insert_machines', views.machines, name="insert_machines"),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('get-token', obtain_auth_token),
    path('home',views.home,name="home"),
    path('dashboard', TemplateView.as_view(template_name='elite_dashboard_main.html'), name="dashboard_main"),
    path('dashboard_sales_tab',TemplateView.as_view(template_name='elite_dashboard_sales_tab.html'),name="dashboard_sales_tab"),
    path('dashboard_tasting_tab',TemplateView.as_view(template_name='dashboard_tasting_tab.html'),name="dashboard_tasting_tab")
]

