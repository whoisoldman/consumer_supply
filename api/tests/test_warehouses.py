# api/tests/test_warehouses.py
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_create_warehouse(api_client, supplier_token):
    url = "/api/warehouses/"
    data = {
        "name": "New Warehouse",
        "address": "181920 Warehouse Street, City, Country"
    }
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {supplier_token}")
    response = api_client.post(url, data, format="json")
    assert response.status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK], f"Warehouse creation failed: {response.content}"
    assert response.data["name"] == "New Warehouse"
    assert response.data["address"] == "181920 Warehouse Street, City, Country"
    assert "id" in response.data, "Warehouse creation response does not contain 'id'"
    assert response.data["owner"] == "supplier1", "Incorrect owner in warehouse data"
