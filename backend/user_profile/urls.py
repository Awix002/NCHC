from django.urls import path
from .views import UserExtraDetails, UserExtraDetailsUpdate

urlpatterns = [
    path('user_extra_details/', UserExtraDetails.as_view(), name='user-extra-details'),
    path('user_extra_details_update/', UserExtraDetailsUpdate.as_view(), name='user-extra-details-update'),
]
