from django.db import models
import datetime


class Gender(models.TextChoices):
	FEMALE = 'F'
	MALE = 'M'
	OTHER = 'O'

class BloodGroup(models.TextChoices):
	A_POSITIVE = 'A+'
	B_POSITIVE = 'B+'
	O_POSITIVE = 'O+'
	AB_POSITIVE = 'AB+'
	A_NEGATIVE = 'A-'
	B_NEGATIVE = 'B-'
	O_NEGATIVE = 'O-'
	AB_NEGATIVE = 'AB-'
	UNKNOWN = 'UKN'
	
class Doctor(models.Model):

	class Expertise(models.TextChoices):
		ALLERGISTS = 'ALG'
		DERMATOLOGIST = 'DRM'
		CARDIOLOGIST = 'CRD'
		OPHTHALMOLOGISTS = 'OPH'
		UNKNOWN = 'UKN'
	
	username = models.CharField(max_length=100, default='Unknown')
	password = models.CharField(max_length=32, default='Unknown')

	email = models.EmailField(unique=True, default='Unknown')
	contact_number = models.CharField(max_length=10, null=True)
	address = models.CharField(max_length=200, null=True)
	
	gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.OTHER)
	dob = models.DateField()
	blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, default=BloodGroup.UNKNOWN)
	
	expertise = models.CharField(max_length=3, choices=Expertise.choices, default=Expertise.UNKNOWN)
	doj = models.DateField(default=datetime.date.today)

	def __str__(self):
		return self.username

class Patient(models.Model):
	username = models.CharField(max_length=100, default='Unknown')
	password = models.CharField(max_length=32, default='Unknown')

	email = models.EmailField(unique=True)
	address = models.CharField(max_length=200, null=True)
	contact_number = models.CharField(max_length=10, null=True)

	gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.OTHER)
	dob = models.DateField(default=datetime.date.today)
	blood_group = models.CharField(max_length=3, choices=BloodGroup.choices, default=BloodGroup.UNKNOWN)

	medical_history = models.CharField(max_length=500, default='Unknown')

	def __str__(self):
		return self.username
	
class DoctorSlot(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=get_doctor_id)
	date = models.DateField()

	slot_count = models.IntegerField(default=0)
	#slot_time = models.JSONField("Time Slots")

	def __str__(self):
		return self.doctor.username+" has "+self.slot_count+" slots available on "+self.date
	
class Appointment(models.Model):
	doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=get_doctor_id)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, default=get_doctor_id)

	appointment_date = models.DateField(default=datetime.date.today)
	appointment_time = models.TimeField(max_length=10)
	register_date = models.DateField(default=datetime.date.today)

	symptoms = models.CharField(max_length=200)
	status = models.BooleanField()
	diagnosis = models.CharField(max_length=500, default='No Diagnosis')
	prescription = models.CharField(max_length=500, default='No Prescriptions')

	def __str__(self):
		return self.patient.username+" you have appointment with "+self.doctor.username

