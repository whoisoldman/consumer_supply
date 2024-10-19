# api/tests/conftest.py
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def supplier_user(db):
    user = User.objects.create_user(
        username="supplier1",
        email="supplier1@example.com",
        password="StrongPassword123",
        user_type="supplier"
    )
    return user

@pytest.fixture
def consumer_user(db):
    user = User.objects.create_user(
        username="consumer1",
        email="consumer1@example.com",
        password="StrongPassword123",
        user_type="consumer"
    )
    return user

@pytest.fixture
def supplier_token(api_client, supplier_user):
    response = api_client.post("/api/login/", {
        "username": "supplier1",
        "password": "StrongPassword123"
    }, format="json")
    assert response.status_code == 200, f"Login failed for supplier: {response.content}"
    return response.data.get("token")

@pytest.fixture
def consumer_token(api_client, consumer_user):
    response = api_client.post("/api/login/", {
        "username": "consumer1",
        "password": "StrongPassword123"
    }, format="json")
    assert response.status_code == 200, f"Login failed for consumer: {response.content}"
    return response.data.get("token")
