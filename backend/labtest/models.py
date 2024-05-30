from django.db import models

class LabTest(models.Model):
    test_name = models.CharField(max_length=255, unique=True)
    unit = models.CharField(max_length=20)
    reference_value = models.CharField(max_length=100)

    def __str__(self):
        return self.test_name
