from django.urls import path
from .views import ChargeWalletView, verify

urlpatterns = [
    path('charge/', ChargeWalletView.as_view(), name="charge"),
    path('verify/', verify,  name="verify"),
]
