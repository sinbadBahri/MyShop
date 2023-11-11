from django.db import models
from django.db.models import CharField
from django.core.exceptions import ValidationError

from mptt.models import MPTTModel, TreeForeignKey

from .fields import OrderField


class ActiveManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).select_related(
            'category', 'brand'
        ).filter(is_active=True)


class Category(MPTTModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150)
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


class Attribute(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=700, blank=True)


class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    product_attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE,
                                          related_name="attribute_values")


class ProductLine(models.Model):
    price = models.PositiveIntegerField()
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product_lines")
    is_available = models.BooleanField(default=False)
    order = OrderField(unique_for_field='product', blank=True)
    attribute_values = models.ManyToManyField(
        AttributeValue, through='ProductLineAttributeValue'
    )

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value !!!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.sku)


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE,
                                        related_name="product_attribute_values_av")
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                                     related_name="product_attribute_values_pl")

    class Meta:
        unique_together = ('attribute_value', 'product_line')


class ProductImage(models.Model):
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE,
                                     related_name="product_images")
    order = OrderField(unique_for_field='product_line', blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(product_line=self.product_line)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value !!!")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.url)
