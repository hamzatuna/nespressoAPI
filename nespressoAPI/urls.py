from django.urls import path, re_path,include
from rest_framework import generics
from . import views

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('get_sales',views.get_sales,name="get_sales"),
    path('insert_sales', views.insert_sales, name="insert_sales"),
    path('insert_tastinginfo',views.TastingInformationsList.as_view(),name='tasting_list')
    #path('get_machines', views.machines, name="get_machines"),
    #path('insert_machines', views.machines, name="insert_machines")
]


