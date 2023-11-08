from django.db import models
from django.db.models import CharField

from mptt.models import MPTTModel, TreeForeignKey


class ActiveManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related(
            'category', 'brand'
        ).filter(is_active=True)


class Temp(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)


class Category(MPTTModel):
    title = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT,
                            related_name="children", null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self) -> CharField:
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self) -> CharField:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="name")
    slug = models.SlugField(max_length=150)
    description = models.TextField(max_length=1000, blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name="products")
    is_active = models.BooleanField(default=False)

    default_manager = models.Manager()
    objects = ActiveManager()

    def __str__(self) -> CharField:
        return self.title


class ProductLine(models.Model):
    price = models.IntegerField()
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_lines")
    is_available = models.BooleanField(default=False)

    def __str__(self) -> CharField:
        return self.sku
