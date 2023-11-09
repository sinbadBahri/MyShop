from rest_framework import serializers

from .models import Category, Brand, Product, ProductLine, ProductImage


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


class ProductLineSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True)

    class Meta:
        model = ProductLine
        fields = (
            'price',
            'sku',
            'stock_qty',
            'order',
            'product_images',
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
