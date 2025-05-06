import pytest
from flasker_sdk.client import FlaskerClient


def test_create_user_invalid_id(client):
    user_data = {
        "id": "123",  # invalid Israeli ID
        "phone": "+972501234567",
        "name": "Bad ID",
        "address": "Somewhere"
    }
    with pytest.raises(Exception) as exc:
        client.create_user(user_data)
    assert exc.value.response.status_code == 400


def test_create_user_invalid_phone(client):
    user_data = {
        "id": "231740706",  # valid ID
        "phone": "0501234567",  # missing '+' prefix
        "name": "Bad Phone",
        "address": "Invalidville"
    }
    with pytest.raises(Exception) as exc:
        client.create_user(user_data)
    assert exc.value.response.status_code == 400


def test_create_user_missing_fields(client):
    user_data = {
        "id": "231740707",
        "phone": "+972501234567"
        # name and address missing
    }
    with pytest.raises(Exception) as exc:
        client.create_user(user_data)
    assert exc.value.response.status_code == 400


def test_create_user_duplicate(client):
    user_data = {
        "id": "231740705",
        "phone": "+972501234567",
        "name": "Duplicate",
        "address": "Same address"
    }
    client.create_user(user_data)
    with pytest.raises(Exception) as exc:
        client.create_user(user_data)
    assert exc.value.response.status_code == 409


def test_get_user_not_found(client):
    with pytest.raises(Exception) as exc:
        client.get_user("000000000")
    assert exc.value.response.status_code == 404


def test_invalid_token_access():
    """Should return 401 when using an invalid token with the SDK."""
    bad_client = FlaskerClient(host="127.0.0.1", port="5003", token="invalid-token")

    with pytest.raises(Exception) as exc_info:
        bad_client.health()

    assert "401" in str(exc_info.value)


def test_missing_token_access():
    """Should return 401 when using no token with the SDK."""
    # Simulate missing token by passing empty string
    no_token_client = FlaskerClient(host="127.0.0.1", port="5003", token="")

    with pytest.raises(Exception) as exc_info:
        no_token_client.health()

    assert "401" in str(exc_info.value)