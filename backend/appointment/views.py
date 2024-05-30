from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Appointment
from .serializers import AppointmentSerializer
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import formats
from django.utils.timezone import localtime
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.db.models import Q

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

class AppointmentCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsPatient)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AppointmentListAPIView(APIView):
    permission_classes = (IsAuthenticated, (IsAdmin | IsReceptionist))

    def get(self, request):
        appointments = Appointment.objects.all()

        # Sorting based on appointment id
        sort_by = request.query_params.get('sort_by', '-id')
        appointments = appointments.order_by(sort_by)
        
        # Filter based on appointment status
        appointment_status = request.query_params.get('appointment_status')
        if appointment_status:
            appointments = appointments.filter(appointment_status=appointment_status)

        # Search based on appointment ID
        search_term = request.query_params.get('search')
        if search_term:
            appointments = appointments.filter(Q(id__icontains=search_term))

        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserAppointmentList(APIView):
    permission_classes = (IsAuthenticated, IsAdmin | IsReceptionist | IsLabTech | IsPatient)

    def get(self, request):
        user_appointments = Appointment.objects.filter(user=request.user, appointment_status__in=['accepted', 'completed']).order_by('-id')
        serializer = AppointmentSerializer(user_appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AppointmentRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer(appointment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                
                # Send confirmation email if appointment status is accepted
                if 'appointment_status' in request.data and request.data['appointment_status'] == 'accepted':
                    self.send_confirmation_email(appointment.user.email, appointment.user.full_name, appointment.appointment_date, appointment.appointment_time, appointment.id)
                
                # Send thank you email if appointment status is completed
                if 'appointment_status' in request.data and request.data['appointment_status'] == 'completed':
                    followup_date = appointment.appointment_date + timedelta(days=30)
                    self.send_thank_you_email(appointment.user.email, appointment.user.full_name, followup_date)

                    # Send follow-up reminder email only three days before the follow-up date
                    reminder_date = followup_date - timedelta(days=29)
                    if reminder_date == localtime().date():  # Check if the reminder date is today
                        self.send_followup_reminder_email(appointment.user.email, appointment.user.full_name, followup_date)
                    
                    # Set follow-up date after 1 month
                    appointment.followup_date = followup_date
                    appointment.save()
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.delete()
            return Response({'message': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def send_confirmation_email(self, user_email, user_full_name, appointment_date, appointment_time, id):
        subject = 'Check-Up Appointment Confirmation - Nepal Classical Homeopathic Clinic'
        message = f'''
Dear {user_full_name},

We are pleased to confirm your upcoming appointment for a check-up at Nepal Classical Homeopathic Clinic.

Appointment Details:
Appointment Id: {id}
Date: {appointment_date}
Time: {appointment_time}

Our team is committed to providing you with the best possible care and service during your visit.
If you have any questions or need to reschedule, please feel free to contact us. We greatly appreciate your trust in us and look forward to seeing you soon.

Kind regards,
Nepal Classical Homeopathic Clinic
'''
        sender = 'nchc.verify@gmail.com'  # Update with your Gmail email address
        recipient = [user_email]
        send_mail(subject, message, sender, recipient, fail_silently=False)
        return Response({'message': 'Confirmation email sent successfully'}, status=status.HTTP_200_OK)

    
    def send_thank_you_email(self, user_email, user_full_name, followup_date):
        subject = 'Thank You for Visiting Nepal Classical Homeopathic Clinic'
        message = f'''
Dear {user_full_name},

Thank you for choosing Nepal Classical Homeopathic Clinic.

As a reminder, your follow-up appointment has been scheduled for {followup_date}. 

Please take note of this date and ensure it fits well into your schedule. Should you require any adjustments or have inquiries, do not hesitate to reach out to us. We trust that your experience with our clinic was satisfactory, and we hope you found our services beneficial. Your health and well-being remain our utmost priority.

We deeply value your trust in our clinic and eagerly anticipate the opportunity to continue supporting your health needs in the future.

Warm regards,
Nepal Classical Homeopathic Clinic
'''
        sender = 'nchc.verify@gmail.com'  # Update with your Gmail email address
        recipient = [user_email]
        send_mail(subject, message, sender, recipient, fail_silently=False)
        return Response({'message': 'Thank you email sent successfully'}, status=status.HTTP_200_OK)
    

#     def send_followup_reminder_email(self, user_email, user_full_name, followup_date):
#         subject = 'Follow-Up Reminder: Your Appointment is Approaching'
                
#         message = f'''
# Dear {user_full_name},

# We hope this email finds you well.

# This is a friendly reminder that your follow-up appointment at Nepal Classical Homeopathic Clinic is scheduled for {formats.date_format(followup_date, "SHORT_DATE_FORMAT")}.

# As a courtesy, we wanted to remind you of your upcoming visit to our clinic. We look forward to seeing you and providing you with the care and attention you deserve.

# Should you need to reschedule or have any questions, please do not hesitate to contact us.

# Kind regards,
# Nepal Classical Homeopathic Clinic
# '''
#         sender = 'nchc.verify@gmail.com'  # Update with your Gmail email address
#         recipient = [user_email]
#         send_mail(subject, message, sender, recipient, fail_silently=False)
#         return Response({'message': 'Follow-up reminder email sent successfully'}, status=status.HTTP_200_OK)
