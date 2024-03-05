from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Gender(models.TextChoices):
    Male = 'Male', 'Male'
    Female = 'Female', 'Female'
    Others = 'Others', 'Others'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=255, choices=Gender.choices, default=Gender.Others)

    def __str__(self):
        return self.user
