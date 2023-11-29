from django.db import models
from django.contrib.auth import get_user_model

from apps.product.models import ProductLine

User = get_user_model()


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="purchases")
    product = models.ForeignKey(ProductLine, on_delete=models.SET_NULL, null=True, related_name="purchases")
    price = models.PositiveBigIntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
