from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
import logging


logger = logging.getLogger('patient_portal.views')



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
        
class PatientView(UserView):
    def registerPatient(request):
        user_details = {}
        flag = ''
        validation = {"error": ''}
        if request.method == 'POST':
            user_details['username'] = request.POST['name']
            user_details['pwd'] = request.POST['password']
            user_details['recheck_pwd'] = request.POST['repeatpassword']
            user_details['contact_number'] = request.POST['phonenumber']
            user_details['email'] = request.POST['email']
            user_details['dob'] = request.POST['dateofbirth']
            user_details['gender'] = request.POST['gender']
            user_details['address'] = request.POST['address']
            user_details['blood_group'] = request.POST['bloodgroup']
			#user_details['medical_history'] = request.POST['medical_history'] #todo :update field names in the UI 
            patient = ""
            validation = user_validation(user_details=user_details)
            try:
				#create new patient
                if not validation["error"]:
                    Patient.objects.create(username=user_details['username'],password=user_details['pwd'],\
											contact_number=user_details['contact_number'],email=user_details['email'],dob=user_details['dob'],\
											gender=user_details['gender'],address=user_details['address'],blood_group=user_details['blood_group'],\
											)#medical_history= user_details['medical_history'])
                    patient = User.objects.create_user(first_name=user_details['username'],email=user_details['email'],\
														password=user_details['pwd'],username=user_details['email'])
                    Group.objects.get_or_create(name='Patient')[0].user_set.add(patient)
                    patient.save()
                    logger.info("Patient is registered")
                    flag = "False"
                    
                else:
                    flag = "True"
            except Exception as e:
                validation["error"].append(str(e))
                flag = "True"
                logger.error("Error when registering patient ", e)
        return render(request,'createaccount.html',{'error':flag})
    
    def addAppointment(request):
        error = ""
        if not request.user.is_active:
            return redirect('loginpage')
        alldoctors = Doctor.objects.all()
        doctor = { 'alldoctors' : alldoctors }
        group = request.user.groups.all()[0].name
        if group == 'Patient':
            if request.method == 'POST':
                doctor_email = request.POST['doctoremail']
                patient_email = request.POST['patientemail']
                appointment_date = request.POST['appointmentdate']
                appointment_time = request.POST['appointmenttime']
                symptoms = request.POST['symptoms']
                print(doctor_email, doctor_email)
                try:
                    doctor = Doctor.objects.filter(email=doctor_email)[0]
                    patient = Patient.objects.filter(email=patient_email)[0]
                    Appointment.objects.create(doctor=doctor,patient=patient,appointment_date=appointment_date,appointment_time=appointment_time,symptoms=symptoms,status=True,prescription="")
                    error = "no"
                except Exception as e:
                    logger.error("Error occurred when registering appointment ", str(e))
                    e = {"error":error}

    def deleteAppointment(request,pid):
     
        if not request.user.is_active:
            return redirect('loginpage')

        try:
            appointment = Appointment.objects.get(id=pid)
            appointment.delete()
			#todo: delete from slot 
        except Exception as e:
            logger.error("Error when deleting appointment ", str(e))
   
        return redirect('viewappointments')

