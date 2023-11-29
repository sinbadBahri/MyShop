from django.db import models, transaction
from django.contrib.auth import get_user_model

from apps.product.models import ProductLine
from apps.finance.models import Payment

User = get_user_model()


class Purchase(models.Model):
    PAID = 10
    NOT_PAID = -10

    STATUS_CHOICES = (
        (PAID, "Paid"),
        (NOT_PAID, "Not paid"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="purchases")
    product = models.ForeignKey(ProductLine, on_delete=models.SET_NULL, null=True, related_name="purchases")
    price = models.PositiveBigIntegerField()
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=NOT_PAID)
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="purchase")
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.user} >> {self.product}"

    @staticmethod
    def create_payment(product, user):
        return Payment.objects.create(amount=product.price, user=user)

    @classmethod
    def create(cls, product, user):
        if product.is_available:

            with transaction.atomic():
                payment = cls.create_payment(product, user)
                purchase = cls.objects.create(user=user, product=product,
                                              price=product.price, payment=payment)
            return purchase

        return None
