from django.urls import path
from .views import ChargeWalletView, verify, VerifyView

urlpatterns = [
    path('charge/', ChargeWalletView.as_view(), name="charge"),
    path('verify/', verify,  name="verify"),
]
