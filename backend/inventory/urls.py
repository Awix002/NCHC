from django.urls import path

from .views import (InventoryListCreateAPIView, InventoryRetrieveUpdateDeleteView)


urlpatterns = [
    path('inventory/', InventoryListCreateAPIView.as_view(), name='inventory-list'),
    path('inventory/<pk>/', InventoryRetrieveUpdateDeleteView.as_view(), name='inventory-retrive'),
]
