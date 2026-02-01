import pytest
from fastapi.testclient import TestClient
from uuid import UUID

from be_task_ca.drivers.rest.app import app
from be_task_ca.drivers.rest.dependencies import (
    get_user_repository,
    get_item_repository,
    get_cart_item_repository,
)
from be_task_ca.adapters.repositories.user.in_memory_user_repository import (
    InMemoryUserRepository,
)
from be_task_ca.adapters.repositories.item.in_memory_item_repository import (
    InMemoryItemRepository,
)
from be_task_ca.adapters.repositories.cart_item.in_memory_cart_item_repository import (
    InMemoryCartItemRepository,
)


@pytest.fixture
def user_repository():
    return InMemoryUserRepository()


@pytest.fixture
def item_repository():
    return InMemoryItemRepository()


@pytest.fixture
def cart_item_repository():
    return InMemoryCartItemRepository()


@pytest.fixture
def client(user_repository, item_repository, cart_item_repository):
    app.dependency_overrides[get_user_repository] = lambda: user_repository
    app.dependency_overrides[get_item_repository] = lambda: item_repository
    app.dependency_overrides[get_cart_item_repository] = lambda: cart_item_repository

    yield TestClient(app)

    app.dependency_overrides.clear()


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "user@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "password123",
            "shipping_address": "123 Main St",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "id" in data
    assert isinstance(UUID(data["id"]), UUID)


def test_create_item(client):
    response = client.post(
        "/items/",
        json={
            "name": "Laptop",
            "description": "A laptop",
            "price": 999.99,
            "quantity": 10,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert "id" in data


def test_get_all_items(client):
    client.post(
        "/items/",
        json={
            "name": "Mouse",
            "description": "A mouse",
            "price": 29.99,
            "quantity": 50,
        },
    )
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_complete_shopping_flow(client):
    user_response = client.post(
        "/users/",
        json={
            "email": "buyer@example.com",
            "first_name": "Alice",
            "last_name": "Smith",
            "password": "password123",
        },
    )
    assert user_response.status_code == 201
    user_id = user_response.json()["id"]

    item_response = client.post(
        "/items/",
        json={
            "name": "Keyboard",
            "description": "Mechanical keyboard",
            "price": 149.99,
            "quantity": 20,
        },
    )
    assert item_response.status_code == 201
    item_id = item_response.json()["id"]

    cart_response = client.post(
        f"/users/{user_id}/cart",
        json={"item_id": item_id, "quantity": 2},
    )
    assert cart_response.status_code == 201

    get_cart_response = client.get(f"/users/{user_id}/cart")
    assert get_cart_response.status_code == 200
    cart = get_cart_response.json()
    assert len(cart) == 1
    assert cart[0]["quantity"] == 2
