from .models import *
from django.shortcuts import render
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.models import User,Group
from django.utils import timezone
# Create your views here.
def home(request):
	return render(request, 'index.html')

def about(request):
	return render(request,'about.html')

def admin_login(request):
	error = ""
	if request.method == 'POST':
		u = request.POST['username']
		p = request.POST['password']
		user = authenticate(username=u,password=p)
		try:
			if user.is_staff:
				login(request,user)
				error = "no"
			else:
				error = "yes"
		except:
			error = "yes"
	d = {'error' : error}
	return render(request,'adminlogin.html',d)

def loginpage(request):
	error = ""
	page = ""
	if request.method == 'POST':
		u = request.POST['email']
		p = request.POST['password']
		user = authenticate(request,username=u,password=p)
		try:
			if user is not None:
				login(request,user)
				error = "no"
				g = request.user.groups.all()[0].name
				if g == 'Doctor':
					page = "doctor"
					d = {'error': error,'page':page}
					return render(request,'doctorhome.html',d)
				elif g == 'Patient':
					page = "patient"
					d = {'error': error,'page':page}
					return render(request,'patienthome.html',d)
			else:
				error = "yes"
		except Exception as e:
			error = "yes"
	
	return render(request,'login.html')

def create_account(request):
	err = ""
	#fetch details from template
	if request.method == 'POST':
		name = request.POST['name']
		pwd = request.POST['password']
		recheck_pwd = request.POST['repeatpassword']
		phone = request.POST['phonenumber']
		mail = request.POST['email']
		dob = request.POST['dateofbirth']
		gender = request.POST['gender']
		address = request.POST['address']
		blood_group = request.POST['bloodgroup']
		medical_history = ""
		new_user = ""

		try:
			#create new account
			if pwd == recheck_pwd:
				Patient.objects.create(username=name,password= pwd,contact_number= phone, email=mail,dob = dob, gender = gender, address = address, blood_group = blood_group, medical_history= medical_history)
				new_user = User.objects.create_user(first_name=name,email=mail,password=pwd,username=mail)
				Group.objects.get(name='Patient').user_set.add(new_user)

				new_user.save()
				err = "False"
			else:
				err = "True"
		except Exception as e:
			err = "True"
	
	return render(request,'createaccount.html',{'error':err})

