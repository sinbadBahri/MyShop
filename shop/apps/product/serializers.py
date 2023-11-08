from rest_framework import serializers

from .models import Category, Brand, Product, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='title')

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        exclude = ('id',)


class ProductLineSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = ProductLine
        exclude = ('id', 'product', 'is_available')


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
