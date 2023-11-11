import factory

from apps.product.models import Category, Brand, Product, ProductLine, ProductImage


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
    is_active = True
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductLine

    price = 1500000
    sku = "YlmYs.8%yc4G"
    stock_qty = 100
    product = factory.SubFactory(ProductFactory)
    is_available = True


class ProductImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductImage

    alternative_text = "test alternative text"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)
