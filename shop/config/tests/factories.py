import factory

from apps.product.models import Category, Brand, Product


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    title = factory.Sequence(lambda x: f"Category object {x}")


class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand

    title = factory.Sequence(lambda x: f"Brand object {x}")


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    description = "lorem"
    is_digital = True
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
