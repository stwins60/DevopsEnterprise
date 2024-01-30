import json
import pytest
from flask import Flask
from app import app, get_products


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_get_product(client):
    products = get_products()
    if not products:
        pytest.skip("No products available to test")
    product_id = products[0]['id']
    response = client.get(f'/products/{product_id}')
    assert response.status_code == 200
    assert isinstance(response.json, dict)

def test_get_product_not_found(client):
    response = client.get('/products/999')
    assert response.status_code == 200
    assert response.json == {'message': 'Product not found'}


def test_add_product(client):
    new_product = {
        'id': 999,
        'name': 'Adidas',
        'price': 50000000.00
    }
    response = client.post('/products', json=new_product)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert new_product in response.json
