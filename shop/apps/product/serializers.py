import modulefinder

from rest_framework import serializers

from .models import (Category, Brand, Product, ProductLine, ProductImage, Attribute, AttributeValue)


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='title')

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        exclude = ('id',)


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        exclude = ('id', 'product_line')


class AttributeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attribute
        fields = ('title',)


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ('attribute', 'attribute_value')


class ProductLineSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)
    attribute_values = AttributeValueSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'price',
            'sku',
            'stock_qty',
            'order',
            'product_images',
            'attribute_values',
        )


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source='brand.title')
    category = CategorySerializer()
    product_lines = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'title',
            'slug',
            'description',
            'brand_name',
            'category',
            'product_lines',
        )
