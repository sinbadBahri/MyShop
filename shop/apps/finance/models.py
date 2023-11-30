import json
import uuid

from django.conf import settings
from django.db import models
from django.db.models import CharField
from django.utils.translation import gettext_lazy as _

from .utils.zarinpal import zarrinpal_request_handler, zarrinpal_payment_checker


class Gateway(models.Model):
    """
    Save gateways name and credentials to the database and use them to handle payments
    """

    FUNCTION_ZARRINPAL = 'zarrinpal'
    FUNCTION_SAMAN = 'saman'
    FUNCTION_PARSIAN = 'parsian'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_IDPAY = 'idpay'
    GATEWAY_FUNCTIONS = (
        (FUNCTION_ZARRINPAL, _('Zarrinpal')),
        (FUNCTION_SAMAN, _('Saman')),
        (FUNCTION_PARSIAN, _('Parsian')),
        (FUNCTION_SHAPARAK, _('Shaparak')),
        (FUNCTION_IDPAY, _('Idpay')),
    )

    title = models.CharField(max_length=100, verbose_name=_("gateway title"))
    gateway_request_url = models.CharField(max_length=100, verbose_name=_("request url"), blank=True, null=True)
    gateway_verify_url = models.CharField(max_length=100, verbose_name=_("verify url"), blank=True, null=True)
    gateway_code = models.CharField(max_length=12, verbose_name=_("gateway code"), choices=GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(verbose_name=_("is enable"), default=True)
    auth_data = models.TextField(verbose_name=_("auth data"), blank=True, null=True)

    class Meta:
        verbose_name = _("Gateway")
        verbose_name_plural = _("Gateways")

    def __str__(self) -> CharField:
        return self.title

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_ZARRINPAL: zarrinpal_request_handler,
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_PARSIAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_IDPAY: None,
        }

        return handlers[self.gateway_code]

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_ZARRINPAL: zarrinpal_payment_checker,
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_PARSIAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_IDPAY: None,
        }

        return handlers[self.gateway_code]

    @property
    def credentials(self):
        return json.loads(self.auth_data)


class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=_("invoice number"), unique=True, default=uuid.uuid4)
    amount = models.PositiveIntegerField(_("payment amount"), editable=True)
    gateway = models.ForeignKey(Gateway, on_delete=models.SET_NULL, related_name="payments",
                                verbose_name=_("gateway"), blank=True, null=True)
    is_paid = models.BooleanField(_("is paid status"), default=False)
    payment_log = models.TextField(_("logs"), blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                             related_name="payments", verbose_name=_("User"))
    authority = models.CharField(max_length=64, verbose_name=_("authority"), blank=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return self.invoice_number.hex

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._b_is_paid = self.is_paid

    def get_handler_data(self, gateway):
        return dict(
            merchant_id=self.gateway.auth_data,
            amount=self.amount,
            description="",
            email=self.user.email,
            mobile=getattr(self.user, 'mobile', None),
            callback_url=settings.ZARRINPAL['gateway_callback_url'],
        )

    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()

        if handler is not None:
            data = self.get_handler_data(self.gateway)
            link, authority = handler(**data)

            if authority is not None:
                self.authority = authority
                self.save()

            return link

    @property
    def title(self):
        return _("Instant payment")

    def status_changed(self):
        return self.is_paid != self._b_is_paid

    def verify(self, data):
        handler = self.gateway.get_verify_handler()

        if not self.is_paid and handler is not None:
            self.is_paid, ref_id = handler(**data)

        return self.is_paid

    def get_gateway(self):
        gateway = Gateway.objects.filter(is_enable=True).first()
        return gateway.gateway_code

    def save_log(self, data, scope='Request handler', save=True):
        generated_log = "test log"

        if self.payment_log != "":
            self.payment_log += generated_log
        else:
            self.payment_log = generated_log

        if save:
            self.save()
