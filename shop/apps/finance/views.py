from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import ChargeWalletForm
from .utils.zarinpal import zarinpal_request_handler


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
            payment_link, authority = zarinpal_request_handler(
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




 # ***********************      Test     **********************


MMERCHANT_ID = "1344b5d4-0048-11e8-94db-005056a205be"  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 15000  # Amount will be based on Toman  Required
description = 'توضیحات تراکنش تستی'  # Required
email = 'user@userurl.ir'  # Optional
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
