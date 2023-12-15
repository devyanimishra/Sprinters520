from django.contrib import admin
from django.urls import path
from hospital.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',homepage,name='homepage'),
    
    path('Login/',UserView.loginUser,name='loginpage'),
    path('logout/',UserView.logoutUser,name='logout'),
    
    path('home/',UserView.home,name='home'),
    path('profile/',UserView.profile,name='profile'),
    
    path('Register/',PatientView.registerPatient,name='registerPatient'),
    path('makeappointments/',PatientView.addAppointment,name='makeappointments'),
    path('viewappointments/',UserView.getAppointment,name='viewappointments'),
    path('PatientDeleteAppointment<int:pid>',PatientView.deleteAppointment,name='patient_delete_appointment'),
    
    path('loginadmin/',AdminView.loginAdmin,name='login_admin'),
    path('HomeAdmin/',AdminView.home,name='HomeAdmin'),
    path('adminlogout/',AdminView.logoutAdmin,name='adminlogout'),
    path('AddDoctorAdmin/',AdminView.registerDoctor,name='AddDoctorAdmin'),
    path('ViewDoctorsAdmin/',AdminView.getDoctor,name='ViewDoctorsAdmin'),
    path('adminDeleteDoctor<int:pid><str:email>',AdminView.deleteDoctor,name='admin_delete_doctor'),
    path('ViewAppointmentAdmin/',AdminView.getAppointment,name='ViewAppointmentAdmin'),
]

