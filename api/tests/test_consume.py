# api/tests/test_consume.py
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_consume_product(api_client, consumer_token, supplier_token):
    # Создаём продукт и склад с помощью поставщика
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {supplier_token}")

    # Создание продукта
    product_response = api_client.post("/api/products/", {
        "name": "Product D",
        "description": "Description of Product D",
        "price": "59.99"
    }, format="json")
    assert product_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Product creation failed: {product_response.content}"
    product = product_response.data
    assert "id" in product, "Product creation response does not contain 'id'"

    # Создание склада
    warehouse_response = api_client.post("/api/warehouses/", {
        "name": "North Warehouse",
        "address": "121314 Warehouse Road, City, Country"
    }, format="json")
    assert warehouse_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Warehouse creation failed: {warehouse_response.content}"
    warehouse = warehouse_response.data
    assert "id" in warehouse, "Warehouse creation response does not contain 'id'"

    # Поставка товара
    supply_response = api_client.post("/api/supply/", {
        "warehouse": warehouse["id"],
        "product": product["id"],
        "quantity": 100
    }, format="json")
    assert supply_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Supply failed: {supply_response.content}"
    assert "quantity" in supply_response.data, "Supply response does not contain 'quantity'"
    assert supply_response.data["quantity"] == 100, "Incorrect quantity after supply"

    # Теперь потребитель изымает товар
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {consumer_token}")
    consume_response = api_client.put("/api/consume/", {
        "warehouse": warehouse["id"],
        "product": product["id"],
        "quantity": 10
    }, format="json")
    assert consume_response.status_code == status.HTTP_200_OK, f"Consume failed: {consume_response.content}"
    assert consume_response.data["quantity"] == 90, "Incorrect quantity after consume"
