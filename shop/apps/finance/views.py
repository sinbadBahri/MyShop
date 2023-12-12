from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View

from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import ChargeWalletForm
from .models import Payment, Gateway

from .utils.zarinpal import zarrinpal_request_handler, zarrinpal_payment_checker

# Test View
# class ChargeWalletView(View):
#     template_name = 'charge_wallet.html'
#     form_class = ChargeWalletForm
#
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name, {'form': self.form_class})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         MMERCHANT_ID = settings.ZARRINPAL['merchant_id']
#         description = ""
#         email = 'aqaSaeed@userurl.ir'  # Optional
#         mobile = '09115006072'  # Optional
#         CallbackURL = settings.ZARRINPAL['gateway_callback_url']
#
#         if form.is_valid():
#             amount = form.cleaned_data['amount']
#             payment_link, authority = zarrinpal_request_handler(
#                         MMERCHANT_ID,
#                         amount,
#                         description,
#                         email,
#                         mobile,
#                         CallbackURL
#                     )
#
#             if payment_link is not None:
#                 print("\n\n*************\n", authority)
#                 print("\n\n***********\n", payment_link)
#                 return redirect(payment_link)
#
#         return render(request, self.template_name, {'form': form})


class VerifyView(View):
    template_name = 'callback.html'

    def get(self, request, *args, **kwargs):
        authority = request.GET['Authority']
        try:
            payment = Payment.objects.get(authority=authority)
        except Payment.DoesNotExist:
            raise Http404

        data = dict(
            merchant_id=payment.gateway.auth_data,
            amount=payment.amount,
            authority=payment.authority,
        )
        payment.verify(data)
        payment.save()

        return render(request, self.template_name, {'payment': payment})


# ********************************          Test 1               *********************************
class PaymentView(View):
    template_name = 'payment.html'

    def get(self, request, invoice_number, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        gateways = Gateway.objects.filter(is_enable=True)

        return render(request, self.template_name, {'payment': payment, 'gateways': gateways})


# ********************************          Test 2               *********************************
class PaymentAPIView(APIView):
    def get(self, request, invoice_number, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        gateways = Gateway.objects.filter(is_enable=True)

        payment_serializer = PaymentSerializer(payment)
        gateway_serializer = GatewaySerializer(gateways, many=True)

        return Response({'payment': payment_serializer.data, 'gateways': gateway_serializer.data})


class PaymentGatewayView(View):
    template_name = 'payment.html'

    def get(self, request, invoice_number, gateway_code, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        try:
            gateway = Gateway.objects.get(gateway_code=gateway_code)
        except Payment.DoesNotExist:
            raise Http404

        payment.gateway = gateway
        payment.save()
        payment_link = payment.bank_page

        if payment_link:
            return redirect(payment_link)

        gateways = Gateway.objects.filter(is_enable=True)
        return render(request, self.template_name, {'payment': payment, 'gateways': gateways})
