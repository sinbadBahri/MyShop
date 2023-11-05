from rest_framework import serializers

from .models import Category, Brand, Product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('title', 'parent')


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('title',)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('title', 'description', 'is_digital', 'brand', 'category')
