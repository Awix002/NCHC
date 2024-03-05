from django.urls import path
from .views import LabTestListCreateAPIView, LabReportListCreateAPIView

urlpatterns = [
    path('lab-tests/', LabTestListCreateAPIView.as_view(), name='lab-test-list-create'),
    path('lab-reports/', LabReportListCreateAPIView.as_view(), name='lab-report-list-create'),
]
