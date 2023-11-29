from django.urls import path
from .views import PurchaseCreateView


urlpatterns = [
    path('create/<int:product_id>/', PurchaseCreateView.as_view())
]