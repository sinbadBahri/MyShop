import requests
from django.conf import settings


def verify_recaptcha(g_token: str) -> bool:
    data = {
        'response': g_token,
        'secret': settings.RECAPTCHA_PRIVATE_KEY
    }

    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result_json = response.json()
    return result_json.get('success') is True
