from django.conf import settings
from suds.client import Client


def zarrinpal_request_handler(merchant_id, amount, description, email, mobile, callback_url):
    client = Client(settings.ZARRINPAL['gateway_request_url'])
    result = client.service.PaymentRequest(
        merchant_id, amount, description, email, mobile, callback_url
    )

    if result.Status == 100:
        return 'https://www.zarinpal.com/pg/StartPay/' + result.Authority, result.Authority
    else:
        return None, None


def zarrinpal_payment_checker(merchant_id, amount, authority):
    client = Client(settings.ZARRINPAL['gateway_request_url'])
    result = client.service.PaymentVerification(merchant_id, amount, authority)
    is_paid = True if result.Status in [100, 101] else False
    return is_paid, result.RefID
