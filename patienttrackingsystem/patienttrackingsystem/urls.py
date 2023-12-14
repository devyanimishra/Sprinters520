from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='homepage'),
    
    path('login/',UserView.loginUser,name='loginpage'),
    path('logout/',UserView.logoutUser,name='logout'),
    
    path('home/',UserView.home,name='home'),
    path('profile/',UserView.profile,name='profile'),
    
]
