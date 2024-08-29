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
async def test_delete_conversation_success(client):
    global conversation_id_list

    conversation_to_delete = conversation_id_list.pop(0)
    delete_response = client.delete(f"/conversations/{conversation_to_delete}")
    assert delete_response.status_code == 204

    get_response_after_delete = client.get(f"/conversations/{conversation_to_delete}")
    assert get_response_after_delete.status_code == 404

@pytest.mark.asyncio
async def test_delete_conversation_not_found(client):
    non_existent_id = "non-existent-id"
    delete_response = client.delete(f"/conversations/{non_existent_id}")
    assert delete_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_conversation_invalid_id(client):
    invalid_id = {"test"}
    delete_response = client.delete(f"/conversations/{invalid_id}")
    assert delete_response.status_code == 404
