from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import LabReport, LabResult
from .serializers import LabReportSerializer, LabResultSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

# Creating custom permissions

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'admin'

class IsReceptionist(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'receptionist'

class IsLabTech(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'labtech'
    
class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role.lower() == 'patient'
    

# for user to view list of their lab reports
class UserLabReportList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_lab_reports = LabReport.objects.filter(user=request.user).order_by('-report_date')
        serializer = LabReportSerializer(user_lab_reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# for user to view details of the specific lab reports
class UserLabReportDetails(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        try:
            lab_report = LabReport.objects.get(id=pk, user=request.user)
            lab_results = LabResult.objects.filter(lab_report=lab_report)
            lab_report_serializer = LabReportSerializer(lab_report)
            lab_results_serializer = LabResultSerializer(lab_results, many=True)
            data = {
                "lab_report": lab_report_serializer.data,
                "lab_results": lab_results_serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except LabReport.DoesNotExist:
            return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# for staff to view details of the specific lab reports of all the users
class LabReportDetails(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

    def get(self, request, pk):
        try:
            lab_report = LabReport.objects.get(id=pk)
            lab_results = LabResult.objects.filter(lab_report=lab_report)
            
            lab_report_serializer = LabReportSerializer(lab_report)
            lab_results_serializer = LabResultSerializer(lab_results, many=True)

            data = {
                "lab_report": lab_report_serializer.data,
                "lab_results": lab_results_serializer.data
            }

            return Response(data, status=status.HTTP_200_OK)
        except LabReport.DoesNotExist:
            return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# for staff to update the details of lab reports such as lab tests and lab results
class LabReportUpdateDetails(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech))

    def put(self, request, pk):
        try:
            lab_report = LabReport.objects.get(id=pk)
            lab_report_serializer = LabReportSerializer(lab_report, data=request.data)

            if lab_report_serializer.is_valid():
                lab_report_serializer.save()

                # Update associated lab results
                lab_results_data = request.data.get('lab_results', [])
                for lab_result_data in lab_results_data:
                    lab_result_id = lab_result_data.get('id')
                    if lab_result_id:
                        lab_result = LabResult.objects.get(id=lab_result_id)
                        lab_result_serializer = LabResultSerializer(lab_result, data=lab_result_data)
                        if lab_result_serializer.is_valid():
                            lab_result_serializer.save()

                return Response(lab_report_serializer.data, status=status.HTTP_200_OK)
            return Response(lab_report_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LabReport.DoesNotExist:
            return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
        except LabResult.DoesNotExist:
            return Response({'error': 'Lab result not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
# for staff to view list and create lab reports for users
class LabReportListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

    def get(self, request):
        search_term = request.query_params.get('search', None)
        lab_reports = LabReport.objects.all().order_by('-id')
        if search_term:
            lab_reports = lab_reports.filter(Q(id__icontains=search_term))
        serializer = LabReportSerializer(lab_reports, many=True)
        return Response(serializer.data)
    
    
    def post(self, request):
        serializer = LabReportSerializer(data=request.data)
        if serializer.is_valid():
            lab_report = serializer.save()

            # Send notification email to the user
            self.send_notification_email(lab_report.user.email, lab_report.id, lab_report.user.full_name)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_notification_email(self, user_email, lab_report_id, full_name):
        subject = 'New Lab Report Created'
        message = f'''
Dear {full_name},

A new lab report (ID: {lab_report_id}) has been created for you. Please log in to view it.

To view your lab report, please click on this link: http://localhost:3000/login

If you have any questions or concerns, please feel free to contact us.

Kind regards,
Nepal Classical Homeopathic Clinic
'''
        sender = settings.EMAIL_HOST_USER  # Update with your sender email
        recipient = [user_email]
        send_mail(subject, message, sender, recipient, fail_silently=False)


# for staff to update and delete the 
class LabReportRetrieveUpdateDeleteView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

    def get(self, request, pk):
        try:
            lab_report = LabReport.objects.get(id=pk)
            serializer = LabReportSerializer(lab_report)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LabReport.DoesNotExist:
            return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            lab_report = LabReport.objects.get(id=pk)
            serializer = LabReportSerializer(lab_report, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LabReport.DoesNotExist:
            return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            lab_report = LabReport.objects.get(id=pk)
            serializer = LabReportSerializer(lab_report, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LabReport.DoesNotExist:
            return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            lab_report = LabReport.objects.get(id=pk)
            lab_report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LabReport.DoesNotExist:
            return Response({'error': 'Lab report not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# APIs Lab Result - Extra 
class LabResultListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

    def get(self, request):
        lab_results = LabResult.objects.all()
        serializer = LabResultSerializer(lab_results, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LabResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LabResultRetrieveUpdateDeleteView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsLabTech | IsPatient))

    def get(self, request, pk):
        try:
            lab_result = LabResult.objects.get(id=pk)
            serializer = LabResultSerializer(lab_result)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except LabResult.DoesNotExist:
            return Response({'error': 'Lab result not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, pk):
        try:
            lab_result = LabResult.objects.get(id=pk)
            serializer = LabResultSerializer(lab_result, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LabResult.DoesNotExist:
            return Response({'error': 'Lab result not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            lab_result = LabResult.objects.get(id=pk)
            serializer = LabResultSerializer(lab_result, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except LabResult.DoesNotExist:
            return Response({'error': 'Lab result not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            lab_result = LabResult.objects.get(id=pk)
            lab_result.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LabResult.DoesNotExist:
            return Response({'error': 'Lab result not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)