# api/tests/test_stocks.py
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_view_stocks(api_client, supplier_token):
    # Создаём продукт, склад и поставку с помощью поставщика
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {supplier_token}")

    # Создание продукта
    product_response = api_client.post("/api/products/", {
        "name": "Product F",
        "description": "Description of Product F",
        "price": "49.99"
    }, format="json")
    assert product_response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Product creation failed: {product_response.content}"
    product = product_response.data
    assert "id" in product, "Product creation response does not contain 'id'"

    # Создание склада
    warehouse_response = api_client.post("/api/warehouses/", {
        "name": "South Warehouse",
        "address": "151617 Warehouse Avenue, City, Country"
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

    # Просмотр запасов
    url = "/api/stocks/"
    response = api_client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK, f"Failed to view stocks: {response.content}"
    assert isinstance(response.data, list), "Stocks response is not a list"
    assert len(response.data) >= 1, "No stocks found"

    # Проверяем, что один из запасов соответствует созданным данным
    stock = next((s for s in response.data if s["warehouse"] == warehouse["id"] and s["product"] == product["id"]), None)
    assert stock is not None, "Stock entry not found"
    assert stock["quantity"] == 100, "Incorrect stock quantity"
