# labreport/serializers.py
from rest_framework import serializers
from .models import LabTest, LabReport

class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['id', 'name', 'unit', 'reference_value'] 

class LabReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabReport
        fields = '__all__'
