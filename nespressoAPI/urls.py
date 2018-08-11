from django.urls import path, re_path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('get_sales',views.get_sales, name="get_sales"),
    # path('insert_sales', views.insert_sales, name="insert_sales"),
    path('get_machines', views.machines, name="get_machines"),
    path('users/register/', views.register_user, name="register"),
    path('insert_machines', views.machines, name="insert_machines"),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('get-token', obtain_auth_token),

]

