from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    
    PATIENT_TYPE_CHOICES = (
        ('new', 'New'),
        ('old', 'Old'),
    )
    patient_type = models.CharField(max_length=10, choices=PATIENT_TYPE_CHOICES, default='new')
    
    APPOINTMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
    )
    appointment_status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS_CHOICES, default='pending')


    APPOINTMENT_TIME_CHOICES = [
        ('10:00 AM', '10:00 AM'),
        ('10:30 AM', '10:30 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:30 AM', '11:30 AM'),
        ('12:00 PM', '12:00 PM'),
        ('12:30 PM', '12:30 PM'),
        ('01:00 PM', '01:00 PM'),
        ('01:30 PM', '01:30 PM'),
        ('02:00 PM', '02:00 PM'),
        ('02:30 PM', '02:30 PM'),
        ('03:00 PM', '03:00 PM'),
        ('03:30 PM', '03:30 PM'),
        ('04:00 PM', '04:00 PM'),
        ('04:30 PM', '04:30 PM'),
    ]

    appointment_time = models.CharField(max_length=10, choices=APPOINTMENT_TIME_CHOICES)    
    appointment_date = models.DateField()    
    phone_number = models.CharField(max_length=50)
    appointment_sent_date = models.DateField(auto_now_add=True)
    followup_date = models.DateField(null=True, blank=True)
