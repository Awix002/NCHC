from django.db import models
from django.contrib.auth import get_user_model
import datetime
from labtest.models import LabTest

User = get_user_model()

class LabReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sample_received_date = models.DateField()
    referenced_by = models.CharField(max_length=255)
    report_date = models.DateField(default=datetime.date.today)
    
    def __str__(self):
        return self.user.full_name

class LabResult(models.Model):
    lab_report = models.ForeignKey(LabReport, on_delete=models.CASCADE)
    lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.lab_report.user.full_name} - {self.lab_test.test_name}"