from django.contrib import admin
from .models import LabReport, LabResult

class LabResultInline(admin.TabularInline):
    model = LabResult
    extra = 1

@admin.register(LabReport)
class LabReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'sample_received_date', 'referenced_by', 'report_date')
    inlines = [LabResultInline]

@admin.register(LabResult)
class LabResultAdmin(admin.ModelAdmin):
    list_display = ('lab_report', 'lab_test', 'result')
