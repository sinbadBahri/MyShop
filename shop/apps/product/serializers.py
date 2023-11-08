from rest_framework import serializers

from .models import Category, Brand, Product, ProductLine


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'parent')


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        exclude = ('id',)


class ProductLineSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()

    class Meta:
        model = ProductLine
        exclude = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    brand = BrandSerializer()
    product_lines = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('id',)
