from django.test import TestCase, Client
from .models import *
from .views import * 
# Create your tests here.
class Tests(TestCase):


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
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_patient_login_view(self):
        client = Client()
        response = client.get('/login/')
        self.assertTemplateUsed(response, 'Login.html')

    def test_admin_login(self):
        client = Client()
        response = client.get('/loginadmin/')
        self.assertTemplateUsed(response, 'LoginAdmin.html')