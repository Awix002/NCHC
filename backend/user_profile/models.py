from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Gender(models.TextChoices):
    Male = 'Male', 'Male'
    Female = 'Female', 'Female'
    Others = 'Others', 'Others'

class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    province_state_name = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=255, default='')    
    address = models.CharField(max_length=255, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, choices=Gender.choices, default=Gender.Others)

    def __str__(self):
        return self.user
