import pytest

conversation_id = None


@pytest.fixture(scope="module", autouse=True)
async def setup_and_teardown_conversation(client):
    global conversation_id

    payload = {"name": "Conversation 1"}
    post_response = client.post("/conversations", json=payload)
    assert post_response.status_code == 201
    conversation_id = post_response.json()["id"]

    yield

    if conversation_id:
        delete_response = client.delete(f"/conversations/{conversation_id}")
        assert delete_response.status_code == 204


@pytest.mark.asyncio
async def test_get_conversation(client):
    global conversation_id

    get_response = client.get(f"/conversations/{conversation_id}")
    assert get_response.status_code == 200

    get_response_data = get_response.json()
    assert get_response_data["id"] == conversation_id
    assert get_response_data["name"] == "Conversation 1"


@pytest.mark.asyncio
async def test_get_conversation_dont_exist(client):
    get_response = client.get(f"/conversations/12345")

    assert get_response.status_code == 404
