from django.urls import path, re_path,include
from rest_framework import generics
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from django.views.generic import TemplateView


urlpatterns = [
    path('', TemplateView.as_view(template_name='login.html')),
    path('login', views.login_site,name="login"),
    path('logout', views.logout_site,name="logout"),

    path('register', views.RegisterUser.as_view()),
    path('register/personnel', views.RegisterPersonnel.as_view()),
    #path('insert_sales', views.insert_sales, name="insert_sales"),
    path(
        'insert_tastinginfo',
        views.TastingInformationsList.as_view(),
        name='tasting_list'
    ),
    path('sales', views.SalesListCreate.as_view(), name="sales_list"),
    path('insert_tastinginfo',views.TastingInformationsList.as_view(),name='tasting_list'),
    path('admin_get_sales',views.SalesListCreate.as_view(), name="get_sales"),
    path('admin_get_tasting_informations',views.TastingInformationsList.as_view(),name='tasting_list'),
    path('get_sales_count',views.get_sales_count,name="get_sales_count"),

    path('get_machines', views.MachinesListCreate.as_view(), name="get_machines"),
    path('get_locations', views.LocationsListCreate.as_view(), name="get_locations"),
    path('get_filtered_sales', views.get_filtered_sales, name="get_filtered_sales"),

    path('get_personnels',views.PersonnelsListCreate.as_view(),name="get_personnels"),
    path('locations/', views.LocationListCreate.as_view(), name="locations"),
    path('locations/<int:pk>/', views.LocationDetail.as_view(), name="locations_detail"),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('get-token', views.CustomObtainAuthToken.as_view(), name="get-token"),



    path('home',views.home,name="home"),
    #path('dashboard', TemplateView.as_view(template_name='dashboard_main.html'), name="dashboard_main"),
    path('dashboard', views.dashboard_main, name="dashboard_main"),
    path('dashboard_sales_tab',TemplateView.as_view(template_name='dashboard_sales_tab.html'),name="dashboard_sales_tab"),
    path('dashboard_add_location', views.dashboard_add_location, name="dashboard_add_location"),
    path('dashboard_add_machine', views.dashboard_add_machine, name="dashboard_add_machine"),
    path('dashboard_add_personnel', views.dashboard_add_personnel, name="dashboard_add_personnel"),
    path('dashboard_add_stock', views.dashboard_add_stock,name="dashboard_add_stock"),
    path('dashboard_add_sales_target', views.dashboard_add_sales_target,name="dashboard_add_sales_target"),

    path('dashboard_tasting_tab',TemplateView.as_view(template_name='dashboard_tasting_tab.html'),name="dashboard_tasting_tab"),
    path('goals', views.CustomerGoalListCreate.as_view()),
    path('stocks', views.StockListCreate.as_view())

]

