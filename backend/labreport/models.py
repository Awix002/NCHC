# labreport/models.py
from django.db import models

class LabTest(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)  # CharField for textual representation
    reference_value = models.CharField(max_length=100)  # Reference value for the test

    def __str__(self):
        return self.name

class LabReport(models.Model):
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return f"{self.test.name} - {self.result} ({self.test.unit}, Ref: {self.test.reference_value})"
