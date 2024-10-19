# api/tests/test_supply.py
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_supply_product(api_client, supplier_token):
    # Предварительно создаем продукт и склад
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {supplier_token}")

    # Создание продукта
    product_response = api_client.post("/api/products/", {
        "name": "Product G",
        "description": "Description of Product G",
        "price": "49.99"
    }, format="json")
    assert product_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Product creation failed: {product_response.content}"
    product = product_response.data
    assert "id" in product, "Product creation response does not contain 'id'"

    # Создание склада
    warehouse_response = api_client.post("/api/warehouses/", {
        "name": "Central Warehouse",
        "address": "1234 Warehouse Lane, City, Country"
    }, format="json")
    assert warehouse_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Warehouse creation failed: {warehouse_response.content}"
    warehouse = warehouse_response.data
    assert "id" in warehouse, "Warehouse creation response does not contain 'id'"

    # Поставка товара
    url = "/api/supply/"
    data = {
        "warehouse": warehouse["id"],
        "product": product["id"],
        "quantity": 100
    }
    supply_response = api_client.post(url, data, format="json")
    assert supply_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Supply failed: {supply_response.content}"
    assert "id" in supply_response.data, "Supply response does not contain 'id'"
    assert supply_response.data["quantity"] == 100, "Incorrect quantity after supply"
