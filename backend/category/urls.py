from django.urls import path
from .views import CategoryListCreateAPIView, CategoryRetrieveUpdateDeleteView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDeleteView.as_view(), name='category-retrieve-update-delete'),
]
