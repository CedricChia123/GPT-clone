import pytest

conversation_id_list = []

@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown_conversation(client):
    global conversation_id_list

    payload1 = {
        "name": "Conversation 1"
    }
    post_response = client.post("/conversations", json=payload1)
    assert post_response.status_code == 201
    conversation_id_list.append(post_response.json()["id"])

    yield

    for conversation_id in conversation_id_list:
        delete_response = client.delete(f"/conversations/{conversation_id}")
        assert delete_response.status_code == 204

@pytest.mark.asyncio
async def test_update_conversation_success(client):
    global conversation_id_list

    conversation_to_update = conversation_id_list[0]

    updated_payload = {
        "name": "Updated Conversation",
        "params": {
            "temperature": 0.8
        }
    }
    put_response = client.put(f"/conversations/{conversation_to_update}", json=updated_payload)
    assert put_response.status_code == 204

    get_response = client.get(f"/conversations/{conversation_to_update}")
    assert get_response.status_code == 200
    get_response_data = get_response.json()
    assert get_response_data["name"] == updated_payload["name"]

@pytest.mark.asyncio
async def test_update_conversation_not_found(client):
    # Attempt to update a non-existent conversation should return 404
    non_existent_id = "non-existent-id"
    updated_payload = {
        "name": "This Won't Work"
    }
    put_response = client.put(f"/conversations/{non_existent_id}", json=updated_payload)
    assert put_response.status_code == 404

@pytest.mark.asyncio
async def test_update_conversation_invalid_payload(client):
    global conversation_id_list

    conversation_to_update = conversation_id_list[0]

    invalid_payload = {
        "name" : 123
    }
    put_response = client.put(f"/conversations/{conversation_to_update}", json=invalid_payload)
    assert put_response.status_code == 400
