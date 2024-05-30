from django.urls import path
from .views import FeedbackListCreateAPIView

urlpatterns = [
    path('feedbacks/', FeedbackListCreateAPIView.as_view(), name='feedback-list-create'),
    path('feedbacks/<int:pk>/', FeedbackListCreateAPIView.as_view(), name='feedback-delete'),
]
