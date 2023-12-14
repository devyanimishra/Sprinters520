from django.db import models
import datetime
# Create your models here.

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
class Gender(models.TextChoices):
	FEMALE = 'F'
	MALE = 'M'
	OTHER = 'O'
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