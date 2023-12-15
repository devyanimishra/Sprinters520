"""PatientTrackerSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='homepage'),
    #path('about/',aboutpage,name='aboutpage'),
    
    path('login/',UserView.loginUser,name='loginpage'),
    path('logout/',UserView.logoutUser,name='logout'),
    
    path('home/',UserView.home,name='home'),
    path('profile/',UserView.profile,name='profile'),
    
    path('createaccount/',PatientView.registerPatient,name='registerPatient'),
    path('makeappointments/',PatientView.addAppointment,name='makeappointments'),
    path('viewappointments/',UserView.getAppointment,name='viewappointments'),
    path('PatientDeleteAppointment<int:pid>',PatientView.deleteAppointment,name='patient_delete_appointment'),
    
    path('loginadmin/',AdminView.loginAdmin,name='login_admin'),
    path('adminhome/',AdminView.home,name='adminhome'),
    path('adminlogout/',AdminView.logoutAdmin,name='adminlogout'),
    path('adminaddDoctor/',AdminView.registerDoctor,name='adminaddDoctor'),
    path('adminviewDoctor/',AdminView.getDoctor,name='adminviewDoctor'),
    path('adminDeleteDoctor<int:pid><str:email>',AdminView.deleteDoctor,name='admin_delete_doctor'),
    path('adminviewAppointment/',AdminView.getAppointment,name='adminviewAppointment'),
]

