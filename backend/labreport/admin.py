# labreport/admin.py
from django.contrib import admin
from .models import LabTest, LabReport

class LabTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'unit', 'reference_value')
    search_fields = ('name',)
    list_per_page = 25

class LabReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'result')
    list_display_links = ('id', 'test')
    search_fields = ('test__name', 'result')
    list_per_page = 25

admin.site.register(LabTest, LabTestAdmin)
admin.site.register(LabReport, LabReportAdmin)
