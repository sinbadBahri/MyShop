import pytest

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
