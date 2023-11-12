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
        fields = ('title', 'id')


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
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        attr_value_data = data.pop('attribute_values')
        attr_values = {}
        for key in attr_value_data:
            attr_values.update({key['attribute']['title']: key['attribute_value']})

        data.update({'specifications': attr_values})
        return data


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
