from django.test import TestCase, Client,RequestFactory
from .models import *
from .views import * 
import django
import datetime
import logging
from django.urls import reverse
from django.shortcuts import get_object_or_404
#from .helper.validation import user_validation
django.setup()
# Create your tests here.

logger = logging.getLogger('patienttrackingsystem.hospital.tests')
class Tests(TestCase):
    
    def setUp(self):
        Patient.objects.create(username="user1",password="pwd1",\
                                contact_number="4132432134",email="user1@gmail.com",dob="1999-01-01",\
                                gender="M",address="Amherst",blood_group='O+')
        Doctor.objects.create(username="user2",password="pwd2",\
                                contact_number="4132432135",email="user2@gmail.com",dob="1999-01-01",\
                                gender="M",address="Amherst",blood_group='O+',expertise='Cardiologist')
        user1 = User.objects.create(username='user1')
        user1.set_password('pwd1')
        user1.save()
        Group.objects.get_or_create(name='Patient')[0].user_set.add(user1)
        user2 = User.objects.create(username='user2')
        user2.set_password('pwd2')
        user2.save()
        Group.objects.get_or_create(name='Doctor')[0].user_set.add(user2)
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpassword',
            email='admin@example.com'
        )
        #Appointment.objects.create(doctor=0,patient=0,appointment_date=appointment_date,appointment_time=appointment_time,symptoms=symptoms,status=True,prescription="")

    def test_home_page(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_account(self):
        data = {
            'username': 'test',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'address': 'Test Address',
            'contact_number': '1234567890',
            'gender': 'M',
            'dob': '1990-01-01',
            'blood_group': 'A+',
        }
        PatientView.add_new_user(data)
        #add_account(data)
        exists = Patient.objects.filter(username=data['username'])
        self.assertTrue(exists)
    
    def test_create_account_page(self):
        client = Client()
        response = client.get('/Register/')
        self.assertEqual(response.status_code, 200)
    
    def test_patient_login_loading(self):
        client = Client()
        response = client.get('/Login/')
        self.assertEqual(response.status_code, 200)

    def test_patient_login_view(self):
        client = Client()
        response = client.get('/Login/')
        self.assertTemplateUsed(response, 'Login.html')

    def test_admin_login(self):
        client = Client()
        response = client.get('/loginadmin/')
        self.assertTemplateUsed(response, 'LoginAdmin.html')
        
    def test_add_appointment(self):
        client = Client()
        client.login(username="user1", password="pwd1")
        data = {
            'doctoremail': 'user2@gmail.com',
            'patientemail': 'user1@gmail.com',
            'appointmentdate': datetime.date.today(),
            'appointmenttime': datetime.time(16,00),#datetime.datetime.now()),
            'symptoms': "test_symptoms"
        }
        # check rendered template for post
        response = client.post('/makeappointments/', data)
        self.assertTemplateUsed(response, 'MakeAppointmentPatient.html')
        
        # check AppointmentDB
        appointment = Appointment.objects.filter(doctor__email=data['doctoremail'], patient__email=data['patientemail'])[0]
        self.assertNotEqual(appointment, [])
        
        # check rendered template for get
        response = client.get('/makeappointments/', data)
        self.assertTemplateUsed(response, 'MakeAppointmentPatient.html')
        
    def test_admin_login_creds(self):
        client = Client()
        self.assertTrue(client.login(username='admin', password='adminpassword'))

    def test_logout(self):
        client = Client()
        client.login(username='admin', password='adminpassword')
        response = client.get('/adminlogout/')
        self.assertEquals(response.status_code,302)

    def test_get_appointment_admin(self):
        client = Client()
        client.login(username='admin', password='adminpassword')
        response = client.get('/ViewAppointmentAdmin/')
        self.assertEqual(response.status_code, 200)

    def test_non_admin_view_appointments_redirect(self):
        client = Client()
        client.login(username='user1', password='pwd1')
        response = client.get('/ViewAppointmentAdmin/')
        self.assertRedirects(response, '/loginadmin/', status_code=302, target_status_code=200)

    def test_login_user_doctor(self):
        client = Client()
        response = client.post(reverse(AdminView.loginAdmin), {'username': 'user2', 'password': 'pwd2'})
        self.assertEqual(response.status_code, 200)

    def test_register_existing_user(self):
        client = Client()
        post_data = {
            'name': 'Test Patient',
            'password': 'testpassword',
            'repeatpassword': 'testpassword',
            'phonenumber': '1234567890',
            'email': 'testpatient@example.com',
            'dateofbirth': '1990-01-01',
            'gender': 'Male',
            'address': 'Test Address',
            'bloodgroup': 'O+',
        }
        #PatientView.add_new_user(post_data)
        response = client.post('/Register/', data= post_data)
        self.assertEqual(response.status_code, 200)
        
    def test_admin_home_landing_page(self):
        client = Client()
        client.login(username='admin', password='adminpassword')
        response = client.get('/HomeAdmin/')
        self.assertTemplateUsed(response,'HomeAdmin.html')

    def test_admin_get_doctor(self):
        client = Client()
        client.login(username = 'admin',password ='adminpassword')
        response = client.get('/ViewDoctorsAdmin/')
        self.assertTemplateUsed(response,'ViewDoctorsAdmin.html')

    def test_non_admin_get_doctor(self):
        client = Client()
        client.login(username='user1', password='pwd1')
        response = client.get('/ViewDoctorsAdmin/')
        self.assertRedirects(response, '/loginadmin/', status_code=302, target_status_code=200)

    def test_admin_add_doctor(self):
        client = Client()
        client.login(username = 'admin',password ='adminpassword')
        post_data = {
            'name': 'Test Doctor',
            'password': 'testpassword',
            'repeatpasssword': 'testpassword',
            'email': 'testdoctor@example.com',
            'gender': 'Male',
            'phonenumber': '1234567890',
            'address': 'Test Address',
            'dateofbirth': '1990-01-01',
            'bloodgroup': 'O+',
            'specialization': 'Cardiology',
        }
        response = client.post('/AddDoctorAdmin/', data=post_data)
        self.assertEqual(response.status_code, 200)
      
    def test_patient_logout(self):
        client = Client()
        client.login(username="user1",password = "pwd1")
        response = client.get('/logout/')
        self.assertEquals(response.status_code,302)

    def test_patient_get_appointment_patient(self):
        client = Client()
        client.login(username='user2', password='pwd2')
        response = client.get('/viewappointments/')
        self.assertTemplateUsed(response,'ViewAppointmentDoctor.html')



    def test_login_user(self):
        client = Client()
        post_data = {
            'email': 'random@gmail.com',
            'password': 'random',
        }
        
        response = client.post('/Login/', data=post_data)
        self.assertIn(response.status_code, [200, 302])

    def test_patient_profile(self):
        client = Client()
        client.login(username = "user1",password="pwd1")
        response = client.get('/profile/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'ProfilePatient.html')