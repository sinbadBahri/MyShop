from django.urls import path
from .views import VerifyView, PaymentView, PaymentAPIView, PaymentGatewayView

# temp
urlpatterns = [
    # path('charge/', ChargeWalletView.as_view(), name="charge"),
    path('verify/', VerifyView.as_view(),  name="verify"),
    path('pay/<str:invoice_number>/', PaymentView.as_view(), name="payment"),
    path('pay/<str:invoice_number>/<str:gateway_code>/', PaymentGatewayView.as_view(), name="payment-gateway"),
]
