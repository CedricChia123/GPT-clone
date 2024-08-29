import pytest

conversation_id_list = []


@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown_conversation(client):
    global conversation_id_list

    payload1 = {"name": "Conversation 1"}
    post_response = client.post("/conversations", json=payload1)
    assert post_response.status_code == 201
    conversation_id_list.append(post_response.json()["id"])

    payload2 = {"name": "Conversation 2"}
    post_response2 = client.post("/conversations", json=payload2)
    assert post_response2.status_code == 201
    conversation_id_list.append(post_response2.json()["id"])

    yield

    for conversation_id in conversation_id_list:
        delete_response = client.delete(f"/conversations/{conversation_id}")
        assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_get_conversation(client):
    global conversation_id

    get_response = client.get(f"/conversations")

    assert get_response.status_code == 200

    conversations = get_response.json()

    retrieved_ids = [conversation["id"] for conversation in conversations]

    for conversation_id in conversation_id_list:
        assert conversation_id in retrieved_ids

    assert len(retrieved_ids) >= len(conversation_id_list)


# Delete one and get all conversations again
@pytest.mark.asyncio
async def test_delete_then_get_conversation(client):
    global conversation_id_list

    conversation_to_delete = conversation_id_list.pop(0)
    delete_response = client.delete(f"/conversations/{conversation_to_delete}")
    assert delete_response.status_code == 204

    get_response_after_delete = client.get(f"/conversations")
    assert get_response_after_delete.status_code == 200

    conversations_after_delete = get_response_after_delete.json()
    retrieved_ids_after_delete = [
        conversation["id"] for conversation in conversations_after_delete
    ]

    assert conversation_to_delete not in retrieved_ids_after_delete

    for remaining_id in conversation_id_list:
        assert remaining_id in retrieved_ids_after_delete
