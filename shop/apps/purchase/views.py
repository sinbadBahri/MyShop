from django.http import Http404
from django.shortcuts import render
from django.views import View

from apps.product.models import ProductLine
from .models import Purchase


class PurchaseCreateView(View):
    template_name = 'purchase.html'

    def get(self, request, product_id, *args, **kwargs):
        try:
            product = ProductLine.objects.get(id=product_id)
        except ProductLine.DoesNotExist:
            raise Http404

        purchase = Purchase.create(product, request.user)

        return render(request, self.template_name, {'purchase': purchase})
