from django.urls import path
from .views import ChargeWalletView, verify, PaymentView

# temp
urlpatterns = [
    path('charge/', ChargeWalletView.as_view(), name="charge"),
    path('verify/', verify,  name="verify"),
    path('payment/<str:invoice_number>/', PaymentView.as_view(), name="payment"),
]
