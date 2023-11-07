import factory

from apps.product.models import Category, Brand, Product


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category


class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    description = "lorem"
    is_digital = True
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
