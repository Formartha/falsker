def test_health_check(client):
    """Ensure the /health endpoint is responsive and structured correctly."""
    data = client.health()
    assert data["status"] in ["OK", "DEGRADED"]
    assert "system" in data
    assert "cpu_percent" in data["system"]
    assert "memory" in data["system"]
    assert "disk" in data["system"]


def test_create_and_get_user(client):
    """create and fetch another user and validate content."""
    user_data = {
        "id": "342398765",
        "phone": "+972501234569",
        "name": "Tomer Cohen",
        "address": "12 Rothschild Blvd, Tel Aviv"
    }
    result = client.create_user(user_data)
    assert result["message"] == "User created"

    user = client.get_user("342398765")
    assert user["name"] == "Tomer Cohen"
    assert user["phone"] == "+972501234569"
    assert user["address"] == "12 Rothschild Blvd, Tel Aviv"


def test_list_users(client):
    """Ensure the created user ID is in the users list."""
    user_data = {
        "id": "339677395",
        "phone": "+972501234569",
        "name": "Yoni Cohen",
        "address": "12 Ben Yehuda St, Jerusalem"
    }
    result = client.create_user(user_data)
    assert result["message"] == "User created"
    users = client.list_users()
    assert "339677395" in users["users"]
