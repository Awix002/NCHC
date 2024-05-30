from django.urls import path
from .views import LabTestListCreateAPIView, LabTestRetrieveUpdateDeleteView

urlpatterns = [
    path('labtest/', LabTestListCreateAPIView.as_view(), name='lab-test-list-create'),
    path('labtest/<int:pk>/', LabTestRetrieveUpdateDeleteView.as_view(), name='lab-test-detail'),
]

# Complete Code of Lab Report and Lab Test includeing model view serializer and urls

# from django.db import models
# from django.contrib.auth import get_user_model
# import datetime
# from labtest.models import LabTest

# User = get_user_model()

# class LabReport(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     sample_received_date = models.DateField()
#     referenced_by = models.CharField(max_length=255)
#     report_date = models.DateField(default=datetime.date.today)
#     sent = models.BooleanField(default=False)  # New field to track if the report has been sent
    
#     def __str__(self):
#         return self.user.full_name

# class LabResult(models.Model):
#     lab_report = models.ForeignKey(LabReport, on_delete=models.CASCADE)
#     lab_test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
#     result = models.CharField(max_length=100)

#     def __str__(self):
#         return f"{self.lab_report.user.full_name} - {self.lab_test.test_name}"




# from django.db import models

# class LabTest(models.Model):
#     test_name = models.CharField(max_length=255, unique=True)
#     unit = models.CharField(max_length=20)
#     reference_value = models.CharField(max_length=100)

#     def __str__(self):
#         return self.test_name


# from rest_framework import serializers
# from .models import LabReport, LabResult

# class LabReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabReport
#         fields = '__all__'

# class LabResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabResult
#         fields = '__all__'


# from rest_framework import serializers
# from .models import LabTest

# class LabTestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = LabTest
#         fields = '__all__'


# from django.urls import path
# from .views import (
#     LabReportListCreateAPIView,
#     LabResultListCreateAPIView,
#     LabReportRetrieveUpdateDeleteView,
#     LabResultRetrieveUpdateDeleteView,
#     SendLabReport,
#     UserLabReportList,
#     SentLabReportsAPIView,
# )

# urlpatterns = [
#     path('labreports/', LabReportListCreateAPIView.as_view(), name='labreport-list-create'),
#     path('labreports/<int:pk>/', LabReportRetrieveUpdateDeleteView.as_view(), name='labreport-detail'),
#     path('labresults/', LabResultListCreateAPIView.as_view(), name='labresult-list-create'),
#     path('labresults/<int:pk>/', LabResultRetrieveUpdateDeleteView.as_view(), name='labresult-detail'),
#     path('send_lab_report/', SendLabReport.as_view(), name='send-lab-report'),
#     path('user_lab_reports/', UserLabReportList.as_view(), name='user-lab-reports'),
#     path('sent_lab_reports/', SentLabReportsAPIView.as_view(), name='sent-lab-reports'),
# ]


# from django.urls import path
# from .views import LabTestListCreateAPIView, LabTestRetrieveUpdateDeleteView

# urlpatterns = [
#     path('labtest/', LabTestListCreateAPIView.as_view(), name='lab-test-list-create'),
#     path('labtest/<int:pk>/', LabTestRetrieveUpdateDeleteView.as_view(), name='lab-test-detail'),
# ]

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from .models import LabReport, LabResult
# from .serializers import LabReportSerializer, LabResultSerializer
# from rest_framework.permissions import IsAuthenticated, BasePermission

# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'admin'

# class IsReceptionist(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'receptionist'

# class IsLabTech(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'labtech'
    
# class IsPatient(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'patient'

# class SentLabReportsAPIView(APIView):
#     permission_classes = (permissions.AllowAny)

#     def get(self, request):
#         try:
#             # Retrieve all sent lab reports from the database
#             sent_lab_reports = LabReport.objects.all()
#             # Serialize the lab reports
#             serializer = LabReportSerializer(sent_lab_reports, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class SendLabReport(APIView):
#     permission_classes = (permissions.AllowAny)

#     def post(self, request):
#         try:
#             lab_report_id = request.data.get('lab_report_id')
#             lab_report = LabReport.objects.get(id=lab_report_id)
#             lab_report.sent = True
#             lab_report.save()
#             return Response({'message': 'Lab report sent successfully'}, status=status.HTTP_200_OK)
#         except LabReport.DoesNotExist:
#             return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class UserLabReportList(APIView):
#     permission_classes = (IsAuthenticated, IsPatient)

#     def get(self, request):
#         user_lab_reports = LabReport.objects.filter(user=request.user)
#         serializer = LabReportSerializer(user_lab_reports, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class LabReportListCreateAPIView(APIView):
#     permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))
#     def get(self, request):
#         lab_reports = LabReport.objects.all()
#         serializer = LabReportSerializer(lab_reports, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = LabReportSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LabResultListCreateAPIView(APIView):
#     permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

#     def get(self, request):
#         lab_results = LabResult.objects.all()
#         serializer = LabResultSerializer(lab_results, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = LabResultSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LabReportRetrieveUpdateDeleteView(APIView):
#     permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

#     def get(self, request, pk):
#         lab_report = LabReport.objects.get(id=pk)
#         serializer = LabReportSerializer(lab_report)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         lab_report = LabReport.objects.get(id=pk)
#         serializer = LabReportSerializer(lab_report, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         lab_report = LabReport.objects.get(id=pk)
#         serializer = LabReportSerializer(lab_report, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         lab_report = LabReport.objects.get(id=pk)
#         lab_report.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class LabResultRetrieveUpdateDeleteView(APIView):
#     permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

#     def get(self, request, pk):
#         lab_result = LabResult.objects.get(id=pk)
#         serializer = LabResultSerializer(lab_result)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         lab_result = LabResult.objects.get(id=pk)
#         serializer = LabResultSerializer(lab_result, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         lab_result = LabResult.objects.get(id=pk)
#         serializer = LabResultSerializer(lab_result, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         lab_result = LabResult.objects.get(id=pk)
#         lab_result.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from .models import LabTest
# from django.contrib.auth import get_user_model
# from .serializers import LabTestSerializer
# from rest_framework.permissions import IsAuthenticated, BasePermission

# User = get_user_model()

# class IsAdmin(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'admin'

# class IsReceptionist(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'receptionist'

# class IsLabTech(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'labtech'
    
# class IsPatient(BasePermission):
#     def has_permission(self, request, view):
#         return request.user and request.user.role.lower() == 'patient'

# class LabTestListCreateAPIView(APIView):
#     permission_classes = (IsAuthenticated, IsAdmin | IsLabTech | IsPatient)

#     def get(self, request):
#         lab_tests = LabTest.objects.all()
#         serializer = LabTestSerializer(lab_tests, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = LabTestSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LabTestRetrieveUpdateDeleteView(APIView):
#     permission_classes = (IsAuthenticated, IsAdmin | IsLabTech | IsPatient)

#     def get(self, request, pk):
#         labtest = LabTest.objects.get(id=pk)
#         serializer = LabTestSerializer(labtest)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk):
#         labtest = LabTest.objects.get(id=pk)
#         serializer = LabTestSerializer(labtest, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         labtest = LabTest.objects.get(id=pk)
#         serializer = LabTestSerializer(labtest, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         labtest = LabTest.objects.get(id=pk)
#         labtest.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

