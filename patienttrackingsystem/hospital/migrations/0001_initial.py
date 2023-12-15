# Generated by Django 3.1.12 on 2023-12-14 18:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='Unknown', max_length=100)),
                ('password', models.CharField(default='Unknown', max_length=32)),
                ('email', models.EmailField(default='Unknown', max_length=254, unique=True)),
                ('contact_number', models.CharField(max_length=10, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], default='O', max_length=1)),
                ('dob', models.DateField()),
                ('blood_group', models.CharField(choices=[('A+', 'A Positive'), ('B+', 'B Positive'), ('O+', 'O Positive'), ('AB+', 'Ab Positive'), ('A-', 'A Negative'), ('B-', 'B Negative'), ('O-', 'O Negative'), ('AB-', 'Ab Negative'), ('UKN', 'Unknown')], default='UKN', max_length=3)),
                ('expertise', models.CharField(choices=[('ALG', 'Allergists'), ('DRM', 'Dermatologist'), ('CRD', 'Cardiologist'), ('OPH', 'Ophthalmologists'), ('UKN', 'Unknown')], default='UKN', max_length=3)),
                ('doj', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='Unknown', max_length=100)),
                ('password', models.CharField(default='Unknown', max_length=32)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('contact_number', models.CharField(max_length=10, null=True)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('O', 'Other')], default='O', max_length=1)),
                ('dob', models.DateField(default=datetime.date.today)),
                ('blood_group', models.CharField(choices=[('A+', 'A Positive'), ('B+', 'B Positive'), ('O+', 'O Positive'), ('AB+', 'Ab Positive'), ('A-', 'A Negative'), ('B-', 'B Negative'), ('O-', 'O Negative'), ('AB-', 'Ab Negative'), ('UKN', 'Unknown')], default='UKN', max_length=3)),
                ('medical_history', models.CharField(default='Unknown', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_date', models.DateField(default=datetime.date.today)),
                ('appointment_time', models.TimeField(max_length=10)),
                ('register_date', models.DateField(default=datetime.date.today)),
                ('symptoms', models.CharField(max_length=200)),
                ('status', models.BooleanField()),
                ('diagnosis', models.CharField(default='No Diagnosis', max_length=500)),
                ('prescription', models.CharField(default='No Prescriptions', max_length=500)),
                ('doctor', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hospital.doctor')),
                ('patient', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='hospital.patient')),
            ],
        ),
    ]
