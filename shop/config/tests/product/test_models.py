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
    def test_str_method(self, product_line_factory):
        obj = product_line_factory(sku="sku_test_1234")
        assert obj.__str__() == "sku_test_1234"

    def test_duplicate_order_values(self, product_line_factory, product_factory):
        obj = product_factory()
        product_line_factory(order=1, product=obj)
        with pytest.raises(ValidationError):
            product_line_factory(order=1, product=obj).clean()
