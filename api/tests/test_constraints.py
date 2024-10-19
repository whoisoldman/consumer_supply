# api/tests/test_constraints.py
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_consume_more_than_available(api_client, consumer_token, supplier_token):
    # Создаём продукт, склад и поставку с помощью поставщика
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {supplier_token}")

    # Создание продукта
    product_response = api_client.post("/api/products/", {
        "name": "Product C",
        "description": "Description of Product C",
        "price": "99.99"
    }, format="json")
    assert product_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Product creation failed: {product_response.content}"
    product = product_response.data
    assert "id" in product, "Product creation response does not contain 'id'"

    # Создание склада
    warehouse_response = api_client.post("/api/warehouses/", {
        "name": "West Warehouse",
        "address": "91011 Warehouse Boulevard, City, Country"
    }, format="json")
    assert warehouse_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Warehouse creation failed: {warehouse_response.content}"
    warehouse = warehouse_response.data
    assert "id" in warehouse, "Warehouse creation response does not contain 'id'"

    # Поставка товара
    supply_response = api_client.post("/api/supply/", {
        "warehouse": warehouse["id"],
        "product": product["id"],
        "quantity": 50
    }, format="json")
    assert supply_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Supply failed: {supply_response.content}"

    # Потребитель пытается изъять больше, чем есть
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {consumer_token}")
    consume_response = api_client.put("/api/consume/", {
        "warehouse": warehouse["id"],
        "product": product["id"],
        "quantity": 1000
    }, format="json")
    assert consume_response.status_code == status.HTTP_400_BAD_REQUEST, f"Unexpected status code: {consume_response.status_code}"
    assert "error" in consume_response.data, "Error message not returned"
    assert consume_response.data["error"] == "Недостаточно товара на складе.", "Incorrect error message"

@pytest.mark.django_db
def test_supplier_cannot_consume(api_client, supplier_token):
    # Поставщик пытается изъять товар
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {supplier_token}")
    consume_response = api_client.put("/api/consume/", {
        "warehouse": 1,
        "product": 1,
        "quantity": 10
    }, format="json")
    assert consume_response.status_code == status.HTTP_403_FORBIDDEN, f"Unexpected status code: {consume_response.status_code}"
    assert "detail" in consume_response.data, "Detail message not returned"
    assert consume_response.data["detail"] == "У вас нет прав для выполнения этого действия.", "Incorrect detail message"

@pytest.mark.django_db
def test_consumer_cannot_supply(api_client, consumer_token):
    # Потребитель пытается поставить товар
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {consumer_token}")
    supply_response = api_client.post("/api/supply/", {
        "warehouse": 1,
        "product": 1,
        "quantity": 100
    }, format="json")
    assert supply_response.status_code == status.HTTP_403_FORBIDDEN, f"Unexpected status code: {supply_response.status_code}"
    assert "detail" in supply_response.data, "Detail message not returned"
    assert supply_response.data["detail"] == "У вас нет прав для выполнения этого действия.", "Incorrect detail message"
