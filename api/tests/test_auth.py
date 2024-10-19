# api/tests/test_auth.py
import pytest
from rest_framework import status

@pytest.mark.django_db
def test_supplier_registration(api_client):
    url = "/api/register/"
    data = {
        "username": "supplier2",
        "email": "supplier2@example.com",
        "password": "AnotherStrongPassword123",
        "password2": "AnotherStrongPassword123",
        "user_type": "supplier"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Supplier registration failed: {response.content}"
    assert response.data["user"]["username"] == "supplier2"
    assert response.data["user"]["user_type"] == "supplier"
    assert "token" in response.data

@pytest.mark.django_db
def test_consumer_registration(api_client):
    url = "/api/register/"
    data = {
        "username": "consumer2",
        "email": "consumer2@example.com",
        "password": "AnotherStrongPassword123",
        "password2": "AnotherStrongPassword123",
        "user_type": "consumer"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED, f"Consumer registration failed: {response.content}"
    assert response.data["user"]["username"] == "consumer2"
    assert response.data["user"]["user_type"] == "consumer"
    assert "token" in response.data

@pytest.mark.django_db
def test_supplier_authentication(api_client, supplier_user):
    url = "/api/login/"
    data = {
        "username": "supplier1",
        "password": "StrongPassword123"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK, f"Supplier authentication failed: {response.content}"
    assert "token" in response.data

@pytest.mark.django_db
def test_consumer_authentication(api_client, consumer_user):
    url = "/api/login/"
    data = {
        "username": "consumer1",
        "password": "StrongPassword123"
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK, f"Consumer authentication failed: {response.content}"
    assert "token" in response.data
