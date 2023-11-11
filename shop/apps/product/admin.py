from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import (Category, Product, Brand, ProductLine, ProductImage, Attribute, AttributeValue)


class EditLinkInline(object):
    def edit(self, instance):
        url = reverse(
            f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
            args=[instance.pk],
        )
        if instance.pk:
            link = mark_safe('<a href="{u}">edit</a>'.format(u=url))
            return link
        return ""


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductLineInline(admin.TabularInline, EditLinkInline):
    model = ProductLine
    readonly_fields = ['edit']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue.product_line_attribute_value.through


@admin.register(ProductLine)
class ProductLineAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, AttributeValueInline]


admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
