from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('about/',about,name='about'),
    path('login/',loginpage,name='login'),
    path('createaccount',create_account,name='create_account'),
    path('admin_login/',admin_login,name='admin_login'), 
]
