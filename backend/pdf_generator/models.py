# labreport/models.py
from django.db import models
from pdf_generator.utils import generate_lab_report_pdf

class LabReport(models.Model):
    # Your model fields

    def generate_pdf_report(self):
        report_data = {
            'Test 1': self.test_1_result,
            'Test 2': self.test_2_result,
            # Add more fields as needed
        }
        file_path = f'lab_report_{self.id}.pdf'
        generate_lab_report_pdf(report_data, file_path)
        return file_path
