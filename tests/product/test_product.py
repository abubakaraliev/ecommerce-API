from core.product.models import Product


def test_create_product():
    product = Product(
        id=1,
        identifier="test",
        price="34",
        is_available= True)
    assert product.id == 1
    assert product.identifier == "test"
    assert product.price == "34"
    assert product.is_available == True