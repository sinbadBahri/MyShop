from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View

from .forms import ChargeWalletForm
from .models import Payment, Gateway
from .utils.zarinpal import zarrinpal_request_handler, zarrinpal_payment_checker


class ChargeWalletView(View):
    template_name = 'charge_wallet.html'
    form_class = ChargeWalletForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        MMERCHANT_ID = settings.ZARRINPAL['merchant_id']
        email = 'aqaSaeed@userurl.ir'  # Optional
        mobile = '09115006072'  # Optional
        CallbackURL = settings.ZARRINPAL['gateway_callback_url']

        # 3
        if form.is_valid():
            amount = form.cleaned_data['amount']
            payment_link, authority = zarrinpal_request_handler(
                        MMERCHANT_ID,
                        amount,
                        description,
                        email,
                        mobile,
                        CallbackURL
                    )

            if payment_link is not None:
                print("\n\n*************\n", authority)
                print("\n\n***********\n", payment_link)
                return redirect(payment_link)

        return render(request, self.template_name, {'form': form})


# *************************     Test verify function-based view      **************************
MMERCHANT_ID = "1344b5d4-0048-11e8-94db-005056a205be"  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 15000  # Amount will be based on Toman  Required
description = 'smth'  # Required
email = 'user@example.com'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:8000/finance/verify/'

from suds.client import Client


def verify(request):
    client = Client(ZARINPAL_WEBSERVICE)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.GET['Authority'],
                                                    amount)
        if result.Status == 100:
            return HttpResponse('Transaction success. RefID: ' + str(result.RefID))
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status))
        else:
            return HttpResponse('Transaction failed. Status: ' + str(result.Status))
    else:
        return HttpResponse('Transaction failed or canceled by user')


# *************************     Test Verify class-based view     ************************
#
# class VerifyView(View):
#     template_name = 'callback.html'
#
#     def get(self, request, *args, **kwargs):
#         authority = request.GET.get('Authority')
#         is_paid, ref_id = zarrinpal_payment_checker(
#             settings.ZARRINPAL['merchant_id'], 31206, authority
#         )
#         context = {'is_paid': is_paid, 'ref_id': ref_id}
#
#         return render(request, self.template_name, context=context)


class PaymentView(View):
    template_name = 'payment.html'

    def get(self, request, invoice_number, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        gateways = Gateway.objects.filter(is_enable=True)

        return render(request, self.template_name, {'payment': payment, 'gateways': gateways})


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