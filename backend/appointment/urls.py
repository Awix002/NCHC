from django.urls import path
from .views import (AppointmentCreateAPIView, AppointmentListAPIView, AppointmentRetrieveUpdateDeleteAPIView, UserAppointmentList, )

urlpatterns = [
    path('appointments/', AppointmentListAPIView.as_view(), name='appointment-list'),
    path('appointments/create/', AppointmentCreateAPIView.as_view(), name='appointment-create'),
    path('appointments/<int:pk>/', AppointmentRetrieveUpdateDeleteAPIView.as_view(), name='appointment-detail'),
    path('userappointments/', UserAppointmentList.as_view(), name='appointment-list'),
]
