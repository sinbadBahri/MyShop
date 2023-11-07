from django.db import models
from django.db.models import CharField

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    title = models.CharField(max_length=100)
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
    title = models.CharField(max_length=100)

    def __str__(self) -> CharField:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="name")
    description = models.TextField(max_length=1000, blank=True)
    is_digital = models.BooleanField(default=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name="products")

    def __str__(self) -> CharField:
        return self.title
