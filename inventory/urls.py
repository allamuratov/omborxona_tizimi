from django.urls import path
from .views import InventoryCheckView

urlpatterns = [
    path('inventory-check/', InventoryCheckView.as_view(), name='inventory-check'),
]
