from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
import logging


logger = logging.getLogger('patient_portal.views')

# Create your views here.

def homepage(request):
	return render(request,'index.html')

def aboutpage(request):
	return render(request,'about.html')

class UserView:
    
    def loginUser(request):
        
        error = ""
        page = ""
        if request.method == 'POST':
            email = request.POST['email']
            pwd = request.POST['password']
            user = authenticate(request,username=email,password=pwd)
            #print("AUTHENTICATING", email,pwd)
            try:
                if user is not None:
                    login(request,user)
                    error = "no"
                    group = request.user.groups.all()[0].name
            
                    if group == 'Doctor':
                        page = "doctor"
                        return render(request,'doctorhome.html',{'error': error,'page':page})
                    elif group == 'Patient':
                        page = "patient"
                        return render(request,'patienthome.html',{'error': error,'page':page})
                else:
                    logger.error('User is not there')
                    error = "Invalid Email or Password"
            except Exception as e:
                error = str(e)
                logger.error("Error when logging as User", str(e))
    
        return render(request,'login.html', {'error': error})
    
    def profile(request):
        
        if not request.user.is_active:
            return redirect('loginpage')
        
        group = request.user.groups.all()[0].name
        
        if group == 'Patient':
            patient_details = Patient.objects.all().filter(email=request.user)
            return render(request,'pateintprofile.html',{ 'patient_details' : patient_details })
        elif group == 'Doctor':
            doctor_details = Doctor.objects.all().filter(email=request.user)
            return render(request,'doctorprofile.html',{ 'doctor_details' : doctor_details })
        
    def getAppointment(request):
        
        if not request.user.is_active:
            return redirect('loginpage')
        
        group = request.user.groups.all()[0].name
        
        if group == 'Patient':
            upcomming_appointments = Appointment.objects.filter(patient__email=request.user,appointment_date__gte=timezone.now(),status=True).order_by('appointment_date')
            previous_appointments = Appointment.objects.filter(patient__email=request.user,appointment_date__lt=timezone.now()).order_by('-appointment_date') | Appointment.objects.filter(patient__email=request.user,status=False).order_by('-appointment_date')
            appointments = { "upcomming_appointments" : upcomming_appointments, "previous_appointments" : previous_appointments }
            return render(request,'patientviewappointments.html',appointments)
        
        elif group == 'Doctor':
            if request.method == 'POST':
                prescriptiondata = request.POST['prescription'] #TODO: update in the UI
                idvalue = request.POST['idofappointment']
                Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata,status=False)
            upcomming_appointments = Appointment.objects.filter(doctor__email=request.user,appointment_date__gte=timezone.now(),status=True).order_by('appointment_date')
            previous_appointments = Appointment.objects.filter(doctor__email=request.user,appointment_date__lt=timezone.now()).order_by('-appointment_date') | Appointment.objects.filter(doctor__email=request.user,status=False).order_by('-appointment_date')
            appointments = { "upcomming_appointments" : upcomming_appointments, "previous_appointments" : previous_appointments }
            return render(request,'doctorviewappointment.html',appointments)

    def logoutUser(request):
        
        if not request.user.is_active:
            return redirect('loginpage')
        logout(request)
        return redirect('loginpage')
    
    def home(request):
        
        if not request.user.is_active:
            return redirect('loginpage')
        
        group = request.user.groups.all()[0].name
        if group == 'Doctor':
            return render(request,'doctorhome.html')
        elif group == 'Patient':
            return render(request,'patienthome.html')
