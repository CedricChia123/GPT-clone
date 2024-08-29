from unittest.mock import patch
import pytest


@pytest.mark.asyncio
async def test_create_conversation(client):
    payload = {
        "name": "string",
        "params": {"temperature": 1},
    }

    response = client.post("/conversations", json=payload)

    assert response.status_code == 201
    response_data = response.json()
    assert type(response_data["id"]) == str
    id = response_data["id"]

    delete_response = client.delete(f"/conversations/{id}")
    assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_create_conversation_invalid_input(client):
    payload = {
        "name": 123,
        "params": {"additionalProp1": {}},
    }

    response = client.post("/conversations", json=payload)

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_conversation_missing_name(client):
    payload = {
        "params": {"additionalProp1": {}},
    }

    response = client.post("/conversations", json=payload)

    assert response.status_code == 400
