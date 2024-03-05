from django.urls import path
from .views import RegisterStaffView, AccountRetrieveUpdateDeleteView

urlpatterns = [
    path('register/', RegisterStaffView.as_view(), name='register'),
    path('accounts/<pk>/', AccountRetrieveUpdateDeleteView.as_view(), name='account-detail'),
    
]


