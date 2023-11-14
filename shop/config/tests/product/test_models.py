import pytest

from django.core.exceptions import ValidationError

pytestmark = pytest.mark.django_db


class TestCategoryModel:
    def test_str_method(self, category_factory):
        category = category_factory(title="test_category")
        assert category.__str__() == "test_category"


class TestBrandModel:
    def test_str_method(self, brand_factory):
        brand = brand_factory(title="test_brand")
        assert brand.__str__() == "test_brand"


class TestProductModel:
    def test_str_method(self, product_factory):
        product = product_factory(title="test_product")
        assert product.__str__() == "test_product"


class TestProductLineModel:
    def test_str_method(self, product_line_factory, attribute_value_factory):
        attribute_values = attribute_value_factory(attribute_value="test value")
        obj = product_line_factory(sku="sku_test_1234", attribute_values=attribute_values)
        assert obj.__str__() == "sku_test_1234"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()


class TestProductImageModel:
    def test_str_method(self, product_image_factory):
        obj = product_image_factory(url='test.jpg')
        assert obj.__str__() == "test.jpg"


class TestProductTypeModel:
    def test_str_method(self, product_type_factory, attribute_factory):
        attribute = attribute_factory(title="test attribute")
        obj = product_type_factory.create(title="test_type", attributes=(attribute,))
        assert obj.__str__() == "test_type"


class TestAttributeModel:
    def test_str_method(self, attribute_factory):
        obj = attribute_factory(title="test attribute")
        assert obj.__str__() == "test attribute"


class TestAttributeValueModel:
    def test_str_method(self, attribute_factory, attribute_value_factory):
        attribute = attribute_factory(title="test-attribute")
        obj = attribute_value_factory(attribute_value="test-attribute-value", attribute=attribute)
        assert obj.__str__() == "test-attribute:  test-attribute-value"
