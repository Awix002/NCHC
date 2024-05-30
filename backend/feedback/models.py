from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255, null=True)
    feedback_subject = models.CharField(max_length=255)
    message = models.TextField()
    submission_date = models.DateField(auto_now_add=True) 
