from django.shortcuts import render,redirect
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone
import logging

from .helper.validation import user_validation

logger = logging.getLogger('patient_portal.views')

# Create your views here.

def homepage(request):
	return render(request,'index.html')

class UserView:

	def add_new_user(data):
		if data:
			Patient.objects.create(**data)
			return True
		return False

	def loginUser(request):

		error = ""
		page = ""
		if request.method == 'POST':
			email = request.POST['email']
			pwd = request.POST['password']
			user = authenticate(request,username=email,password=pwd)

			try:
				if user is not None:
					login(request,user)
					group = request.user.groups.all()[0].name
					error = "False"
					if group == 'Doctor':
						page = "doctor"
						return render(request,'HomeDoctor.html',{'error': error,'page':page})
					elif group == 'Patient':
						page = "patient"
						return render(request,'HomePatient.html',{'error': error,'page':page})
				else:
					logger.error('User is not there')
					error = "True"
			except Exception as e:
				error = "True"
				logger.error("Error when logging as User", str(e))
		return render(request,'Login.html', {'error': error})

	def profile(request):
		'''
			Patient and Doctor can view their repective profiles
		'''
		if not request.user.is_active:
			return redirect('loginpage')

		group = request.user.groups.all()[0].name

		if group == 'Patient':
			patient_details = Patient.objects.all().filter(email=request.user)
			return render(request,'ProfilePatient.html',{ 'patient_details' : patient_details })
		elif group == 'Doctor':
			doctor_details = Doctor.objects.all().filter(email=request.user)
			return render(request,'ProfileDoctor.html',{ 'doctor_details' : doctor_details })

	def getAppointment(request):
		'''
		  Patient and Doctor can their repective appointment schedules
		 '''
		if not request.user.is_active:
			return redirect('loginpage')

		group = request.user.groups.all()[0].name

		if group == 'Patient':
			upcoming_appointments = Appointment.objects.filter(patient__email=request.user,appointment_date__gte=timezone.now(),status=True).order_by('appointment_date')
			previous_appointments = Appointment.objects.filter(patient__email=request.user,appointment_date__lt=timezone.now()).order_by('-appointment_date') | Appointment.objects.filter(patient__email=request.user,status=False).order_by('-appointment_date')
			appointments = { "upcoming_appointments" : upcoming_appointments, "previous_appointments" : previous_appointments }
			return render(request,'ViewAppointmentPatient.html',appointments)

		elif group == 'Doctor':
			if request.method == 'POST':
				prescriptiondata = request.POST['prescription']
				idvalue = request.POST['idofappointment']
				Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata,status=False)
			upcoming_appointments = Appointment.objects.filter(doctor__email=request.user,appointment_date__gte=timezone.now(),status=True).order_by('appointment_date')
			previous_appointments = Appointment.objects.filter(doctor__email=request.user,appointment_date__lt=timezone.now()).order_by('-appointment_date') | Appointment.objects.filter(doctor__email=request.user,status=False).order_by('-appointment_date')
			appointments = { "upcoming_appointments" : upcoming_appointments, "previous_appointments" : previous_appointments }
			return render(request,'ViewAppointmentDoctor.html',appointments)

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
			return render(request,'HomeDoctor.html')
		elif group == 'Patient':
			return render(request,'HomePatient.html')

class PatientView(UserView):
    def registerPatient(request):
    '''
            Patient can register on the portal
            '''
        user_details = {}
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
            patient = ""
            validation = user_validation(user_details=user_details)
            try:
				#create new patient
				if not validation["error"]:
					Patient.objects.create(username=user_details['username'],password=user_details['pwd'],\
											contact_number=user_details['contact_number'],email=user_details['email'],dob=user_details['dob'],\
											gender=user_details['gender'],address=user_details['address'],blood_group=user_details['blood_group'])
					patient = User.objects.create_user(first_name=user_details['username'],email=user_details['email'],\
														password=user_details['pwd'],username=user_details['email'])
					Group.objects.get_or_create(name='Patient')[0].user_set.add(patient)
					patient.save()
					validation["error"] = "False"
					logger.info("Patient is registered")
				else:
					validation["error"] = "False"
			except Exception as e:
				validation["error"] = "True"
				logger.error("Error when registering patient ", e)
		return render(request,'Register.html', {'error': validation["error"]})

	def addAppointment(request):
		'''
				Patient can book an appointment
				'''
		if not request.user.is_active:
			return redirect('loginpage')
		alldoctors = Doctor.objects.all()
		doctor = { 'alldoctors' : alldoctors }
		group = request.user.groups.all()[0].name
		err = ''
		if group == 'Patient':
			if request.method == 'POST':
				doctor_email = request.POST['doctoremail']
				patient_email = request.POST['patientemail']
				appointment_date = request.POST['appointmentdate']
				appointment_time = request.POST['appointmenttime']
				symptoms = request.POST['symptoms']
				try:
					doctor = Doctor.objects.filter(email=doctor_email)[0]
					patient = Patient.objects.filter(email=patient_email)[0]
					Appointment.objects.create(doctor=doctor,patient=patient,appointment_date=appointment_date,appointment_time=appointment_time,symptoms=symptoms,status=True,prescription="")
					err = "False"
				except Exception as e:
					logger.error("Error occurred when registering appointment ", str(e))
					err = "True"

				return render(request,'MakeAppointmentPatient.html',{'error':err})
			elif request.method == 'GET':
				return render(request,'MakeAppointmentPatient.html',doctor)

	def deleteAppointment(request,pid):
	 '''
			 Patient can delete the appointment scheduled
			 '''
		if not request.user.is_active:
			return redirect('loginpage')

		try:
			appointment = Appointment.objects.get(id=pid)
			appointment.delete()
		except Exception as e:
			logger.error("Error when deleting appointment ", str(e))
   
		return redirect('viewappointments')


class AdminView:

	def loginAdmin(request):

		error = ''
		if request.method == 'POST':
			username = request.POST['username']
			pwd = request.POST['password']
			print(username, pwd)
			user = authenticate(username=username,password=pwd)

			try:
				if user.is_staff:
					login(request,user)
					error = "False"
				else:
					error = "True"
			except Exception as e:
				error = "True"
				logger.info("Error when logging in as admin ", str(e))
		return render(request,'LoginAdmin.html',{'error': error})

	def registerDoctor(request):
		'''
				Admin can register doctors
				'''
		user_details = {}
		validation = {"error": ''}
		if not request.user.is_staff:
			return redirect('login_admin')

		if request.method == 'POST':
			user_details['username'] = request.POST['name']
			user_details['pwd'] = request.POST['password']
			user_details['recheck_pwd'] =  request.POST['repeatpasssword']
			user_details['email'] = request.POST['email']
			user_details['gender'] = request.POST['gender']
			user_details['contact_number'] = request.POST['phonenumber']
			user_details['address'] = request.POST['address']
			user_details['dob'] = request.POST['dateofbirth']
			user_details['blood_group'] = request.POST['bloodgroup']
			user_details['expertise'] = request.POST['specialization']
			doctor = None
			validation = user_validation(user_details=user_details)

			try:
				if not validation['error']:
					Doctor.objects.create(username=user_details['username'],email=user_details['email'],password=user_details['pwd'],\
											gender=user_details['gender'],contact_number=user_details['contact_number'],address=user_details['address'],\
											dob=user_details['dob'],blood_group=user_details['blood_group'],expertise=user_details['expertise'])
					doctor = User.objects.create_user(first_name=user_details['username'],email=user_details['email'],\
													password=user_details['pwd'],username=user_details['email'])
					Group.objects.get_or_create(name='Doctor')[0].user_set.add(doctor)
					doctor.save()
					validation["error"] = "False"
					logger.info("Doctor is registered")
			except Exception as e:
				validation["error"] = "True"
				logger.error("Error when registering doctor ", str(e))
		return render(request,'AddDoctorAdmin.html',validation)

	def getDoctor(request):
		'''
				Admin can view, search doctors
				'''
		if not request.user.is_staff:
			return redirect('login_admin')
		doctor = None

		try:
			doctor = Doctor.objects.all()
		except Exception as e:
			logger.error("Error when getting doctor ", str(e))

		return render(request,'ViewDoctorsAdmin.html',{ 'doc' : doctor })

	def deleteDoctor(request,pid,email):
		'''
				Admin can delete doctor
				'''
		if not request.user.is_staff:
			return redirect('login_admin')

		try:
			doctor = Doctor.objects.get(id=pid)
			doctor.delete()

			users = User.objects.filter(username=email)
			users.delete()
																																																																																																											
			logger.info("Delete doctor")
		except Exception as e:
			logger.error("Error when deleting doctor ", str(e))

		return redirect('ViewDoctorsAdmin')

	def getAppointment(request):
		'''
				Admin can view all the appointment schedules
				'''
		if not request.user.is_staff:
			return redirect('login_admin')
		try:
			upcoming_appointments = Appointment.objects.filter(appointment_date__gte=timezone.now(),status=True).order_by('appointment_date')
			previous_appointments = Appointment.objects.filter(appointment_date__lt=timezone.now()).order_by('-appointment_date') | Appointment.objects.filter(status=False).order_by('-appointment_date')
			appointments = { "upcoming_appointments" : upcoming_appointments, "previous_appointments" : previous_appointments }
		except Exception as e:
			logger.error("Error when getting the appointments ", str(e))

		return render(request,'ViewAppointmentAdmin.html',appointments)

	def logoutAdmin(request):

		if not request.user.is_staff:
			return redirect('login_admin')
		logout(request)
		return redirect('login_admin')

	def home(request):

		if not request.user.is_staff:#after login user comes to this page.
			return redirect('login_admin')
		return render(request,'HomeAdmin.html')

