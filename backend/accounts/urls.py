from django.urls import path
from .views import (
    StaffAccountCreate,
    StaffAccountList,
    StaffAccountRetrieveUpdateDeleteView,
    UserAccountListAPIView,
    UserAccountRetrieveUpdateDeleteView,
    CheckIsAdmin,
    # UserProfileDetailsAPIView,
    # UserProfileUpdate,

)

urlpatterns = [
    path('staffcreate/', StaffAccountCreate.as_view(), name='staff-create'),
    path('staff/', StaffAccountList.as_view(), name='staff-details'),
    path('staff/<int:pk>/', StaffAccountRetrieveUpdateDeleteView.as_view(), name='account-detail'),
    path('users/', UserAccountListAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserAccountRetrieveUpdateDeleteView.as_view(), name='user-retrieve-update-delete'),
    path('check_is_admin/', CheckIsAdmin.as_view(), name='check_is_admin'),
    # path('user_details/', UserProfileDetailsAPIView.as_view(), name='user_details'),
    # path('update_profile/', UserProfileUpdate.as_view(), name='update-profile'),

]
