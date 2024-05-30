from django.contrib import admin
from .models import LabTest

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'unit', 'reference_value')
