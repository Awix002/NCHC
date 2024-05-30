from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.serializers import serialize
from accounts.models import UserAccount
from appointment.models import Appointment
from category.models import Category
from inventory.models import Inventory
from feedback.models import Feedback
from labtest.models import LabTest
from labreport.models import LabReport, LabResult
from django.db.models.functions import ExtractDay, ExtractWeek, ExtractMonth, ExtractYear
from django.db.models import Count
from django.utils.timezone import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, BasePermission

User = get_user_model()

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

class DashboardData(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsReceptionist | IsLabTech | IsPatient)

    def get(self, request):
        # appointment_list = Appointment.objects.all().order_by('-appointment_date')[:5]
        # serialized_appointments = serialize('json', appointment_list)

        total_staff = UserAccount.objects.filter(is_staff=True).count()
        total_patients = UserAccount.objects.filter(role=UserAccount.PATIENT).count()

        total_appointments = Appointment.objects.count()

        total_items = Inventory.objects.count()

        total_feedbacks = Feedback.objects.count()

        total_lab_reports = LabReport.objects.count()

        data = {
            'total_staff': total_staff,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'total_items': total_items,
            'total_feedbacks': total_feedbacks,
            'total_lab_reports': total_lab_reports,
            # 'appointment_list': serialized_appointments
        }

        return Response(data)

class DashboardDoughnutChart(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsReceptionist | IsLabTech | IsPatient)
    def get(self, request):
        total_receptionists = UserAccount.objects.filter(role=UserAccount.RECEPTIONIST).count()
        total_labtechs = UserAccount.objects.filter(role=UserAccount.LABTECH).count()
        total_admins = UserAccount.objects.filter(role=UserAccount.ADMIN).count()

        data = {
            'total_receptionists': total_receptionists,
            'total_labtechs': total_labtechs,
            'total_admins': total_admins,
        }

        return Response(data)


class DashboardPieChart(APIView):
    permission_classes = (IsAuthenticated, IsAdmin  | IsReceptionist | IsLabTech | IsPatient)
    def get(self, request):
        total_pending_appointments = Appointment.objects.filter(appointment_status='pending').count()
        total_accepted_appointments = Appointment.objects.filter(appointment_status='accepted').count()
        total_completed_appointments = Appointment.objects.filter(appointment_status='completed').count()

        data = {
            'total_pending_appointments': total_pending_appointments,
            'total_accepted_appointments': total_accepted_appointments,
            'total_completed_appointments': total_completed_appointments,
        }

        return Response(data)

class DashboardLineGraph(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsReceptionist | IsLabTech | IsPatient)
    def get(self, request):
        appointments_per_month = Appointment.objects.annotate(
            month=ExtractMonth('appointment_date'),
            year=ExtractYear('appointment_date')
        ).values(
            'year', 'month'
        ).annotate(
            total_appointments=Count('id')
        ).order_by('year', 'month')

        data = {
            'appointments_per_month': list(appointments_per_month)
        }

        return Response(data)



# class DashboardLineGraph(APIView):
#     def get(self, request):
#         # appointments_per_day = Appointment.objects.annotate(
#         #     day=ExtractDay('appointment_date')
#         # ).values(
#         #     'day'
#         # ).annotate(
#         #     total_appointments=Count('id')
#         # ).order_by('day')

#         appointments_per_month = Appointment.objects.annotate(
#             month=ExtractMonth('appointment_date'),
#             year=ExtractYear('appointment_date')
#         ).values(
#             'year', 'month'
#         ).annotate(
#             total_appointments=Count('id')
#         ).order_by('year', 'month')

#         data = {
#             'appointments_per_day': list(appointments_per_day),
#             'appointments_per_month': list(appointments_per_month)
#         }

        return Response(data)
    

# class DashboardLabLineGraph(APIView):
#     def get(self, request):
#         lab_reports_per_day = LabReport.objects.annotate(day=ExtractDay('sample_received_date')).values('day').annotate(total_lab_reports=Count('id'))

#         lab_reports_per_week = LabReport.objects.annotate(week=ExtractWeek('sample_received_date')).values('week').annotate(total_lab_reports=Count('id'))

#         lab_reports_per_month = LabReport.objects.annotate(month=ExtractMonth('sample_received_date')).values('month').annotate(total_lab_reports=Count('id'))

#         data = {
#             'lab_reports_per_day': lab_reports_per_day,
#             'lab_reports_per_week': lab_reports_per_week,
#             'lab_reports_per_month': lab_reports_per_month,
#         }

#         return Response(data)
    
class DashboardLabLineGraph(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsReceptionist | IsLabTech | IsPatient)
    def get(self, request):
        lab_reports_per_month = LabReport.objects.annotate(
            month=ExtractMonth('sample_received_date'),
            year=ExtractYear('sample_received_date')
        ).values('month', 'year').annotate(
            total_lab_reports=Count('id')
        )

        data = {
            'lab_reports_per_month': list(lab_reports_per_month),
        }

        return Response(data)


    
class DashboardInventoryBarChart(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsReceptionist | IsLabTech | IsPatient)
    def get(self, request):
        categories_with_counts = Category.objects.annotate(total_items=Count('inventory'))

        data = {
            'categories': [
                {
                    'category_name': category.category_name,
                    'total_items': category.total_items
                }
                for category in categories_with_counts
            ]
        }

        return Response(data)




class DashboardLabBarChart(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsReceptionist | IsLabTech | IsPatient)
    def get(self, request):
        popular_lab_tests = LabResult.objects.values('lab_test__test_name').annotate(
            total_occurrences=Count('id')
        ).order_by('-total_occurrences')[:5]  # Get the top 5 most popular lab tests

        data = {
            'popular_lab_tests': list(popular_lab_tests)
        }

        return Response(data)


