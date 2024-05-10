from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    admin_field = models.CharField(max_length=50, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

class Receptionist(User):
   patients = models.ManyToManyField('Patient', related_name='receptionists')

class Patient(User):
    pass

User._meta.get_field('groups').remote_field.related_name = 'user_groups'
User._meta.get_field('user_permissions').remote_field.related_name = 'user_permissions'


class Hospital(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    description = models.TextField()
    services_offered = models.TextField()


class Specialist(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    education = models.TextField()
    certifications = models.TextField()   


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    date = models.DateTimeField()
    status = models.CharField(max_length=20, default='Scheduled')  # Add status field
    visit_reason = models.CharField(max_length=150)     