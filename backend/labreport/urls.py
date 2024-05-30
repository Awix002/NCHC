from django.urls import path
from .views import (
    LabReportListCreateAPIView,
    LabResultListCreateAPIView,
    LabReportRetrieveUpdateDeleteView,
    LabResultRetrieveUpdateDeleteView,
    UserLabReportList,
    LabReportDetails,
    LabReportUpdateDetails,
    UserLabReportList,
    UserLabReportDetails,
)

urlpatterns = [
    path('labreports/', LabReportListCreateAPIView.as_view(), name='labreport-list-create'),
    path('labreports/<int:pk>/', LabReportRetrieveUpdateDeleteView.as_view(), name='labreport-detail'),
    path('labresults/', LabResultListCreateAPIView.as_view(), name='labresult-list-create'),
    path('labresults/<int:pk>/', LabResultRetrieveUpdateDeleteView.as_view(), name='labresult-detail'),
    path('user_lab_reports/', UserLabReportList.as_view(), name='user-lab-reports'),
    path('user_lab_reports/<int:pk>/', UserLabReportDetails.as_view(), name='user-lab-report-detail'),
    path('labreports/<int:pk>/details/', LabReportDetails.as_view(), name='labreport-details'),
    path('labreports/<int:pk>/update-details/', LabReportUpdateDetails.as_view(), name='labreport-update-details'),
]