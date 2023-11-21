import pytest

from pytest_factoryboy import register
from rest_framework.test import APIClient

from .factories import (
    # product app
    AttributeFactory,
    AttributeValueFactory,
    BrandFactory,
    CategoryFactory,
    ProductFactory,
    ProductLineFactory,
    ProductImageFactory,
    ProductTypeFactory,

    # user app
    UserFactory,
)

register(AttributeFactory)
register(AttributeValueFactory)
register(BrandFactory)
register(CategoryFactory)
register(ProductFactory)
register(ProductLineFactory)
register(ProductImageFactory)
register(ProductTypeFactory)

register(UserFactory)


@pytest.fixture
def api_client():
    return APIClient
