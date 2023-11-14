import factory

from apps.product.models import (
    Category,
    Brand,
    Product,
    ProductLine,
    ProductImage,
    ProductType,
    Attribute,
    AttributeValue,
)


class CategoryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Category

    title = factory.Sequence(lambda x: f"Category object {x}")


class BrandFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Brand

    title = factory.Sequence(lambda x: f"Brand object {x}")


class AttributeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Attribute

    title = "test attribute"
    description = "lorem"


class ProductTypeFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductType

    title = "test_type"

    @factory.post_generation
    def attributes(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attributes.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Product

    description = "lorem"
    is_digital = True
    is_active = True
    category = factory.SubFactory(CategoryFactory)
    brand = factory.SubFactory(BrandFactory)
    product_type = factory.SubFactory(ProductTypeFactory)


class AttributeValueFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = AttributeValue

    attribute_value = "test attribute value"
    attribute = factory.SubFactory(AttributeFactory)


class ProductLineFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductLine

    price = 1500000
    sku = "YlmYs.8%yc4G"
    stock_qty = 100
    product = factory.SubFactory(ProductFactory)
    is_available = True

    @factory.post_generation
    def attribute_values(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        self.attribute_values.add(extracted)


class ProductImageFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ProductImage

    alternative_text = "test alternative text"
    url = "test.jpg"
    product_line = factory.SubFactory(ProductLineFactory)
