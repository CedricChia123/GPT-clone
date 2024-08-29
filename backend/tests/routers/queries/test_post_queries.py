import pytest

conversation_id = None

@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown_conversation(client):
    global conversation_id

    payload1 = {
        "name": "Conversation 1"
    }
    post_response = client.post("/conversations", json=payload1)
    assert post_response.status_code == 201
    conversation_id = post_response.json()["id"]

    yield

    if conversation_id:
        delete_response = client.delete(f"/conversations/{conversation_id}")
        assert delete_response.status_code == 204

@pytest.mark.asyncio
async def test_create_query(client):
    payload = {
        "role": "user",
        "content": "Hello"
    }

    response = client.post(f"/queries?id={conversation_id}", json=payload)

    assert response.status_code == 201

@pytest.mark.asyncio
async def test_create_query_invalid_input(client):
    payload = {
        "role": "user"
    }

    response = client.post(f"/queries?id={conversation_id}", json=payload)

    assert response.status_code == 400

@pytest.mark.asyncio
async def test_create_query_invalid_id(client):
    payload = {
        "role": "user",
        "content": "Hello"
    }

    response = client.post(f"/queries?id=123", json=payload)

    assert response.status_code == 404

# Create conversation with valid params that openAI can register
@pytest.mark.asyncio
async def test_create_query_with_valid_params(client):
    payload1 = {
        "name": "Invalid Conversation",
        "params": {
            "temperature": 0.8
        }
    }
    post_response = client.post("/conversations", json=payload1)
    assert post_response.status_code == 201
    conversation_id_test_valid = post_response.json()["id"]

    payload = {
        "role": "user",
        "content": "Hello"
    }

    response = client.post(f"/queries?id={conversation_id_test_valid}", json=payload)

    assert response.status_code == 201

    delete_response = client.delete(f"/conversations/{conversation_id_test_valid}")
    assert delete_response.status_code == 204

# Create conversation with invalid params that openAI cannot register
@pytest.mark.asyncio
async def test_create_query_with_invalid_params(client):
    payload1 = {
        "name": "Invalid Conversation",
        "params": {
            "invalid": "invalid"
        }
    }
    post_response = client.post("/conversations", json=payload1)
    assert post_response.status_code == 201
    conversation_id_test = post_response.json()["id"]

    payload = {
        "role": "user",
        "content": "Hello"
    }

    response = client.post(f"/queries?id={conversation_id_test}", json=payload)

    assert response.status_code == 422

    delete_response = client.delete(f"/conversations/{conversation_id_test}")
    assert delete_response.status_code == 204