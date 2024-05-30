from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import datetime
import user_profile

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        email = email.lower()
        
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        profile = user_profile.models.UserProfile(user=user)
        profile.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    registered_date = models.DateField(default=datetime.date.today)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Define choices for roles
    PATIENT = 'patient'
    RECEPTIONIST = 'receptionist'
    LABTECH = 'labtech'
    ADMIN = 'admin'
    PATIENT = 'patient'
    ROLE_CHOICES = [
        (PATIENT, 'Patient'),
        (RECEPTIONIST, 'Receptionist'),
        (LABTECH, 'Lab Technician'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=PATIENT)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number', 'role']

    def get_full_name(self):
        return self.full_name

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return self.email

