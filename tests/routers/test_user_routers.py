from tests.conftest import client, test_db

DATA_USER = {
        "login": "test",
        "first_name": "test",
        "second_name": "test",
        "password": "test"
    }


def test_create_user(test_db):
    response = client.post("/users", json=DATA_USER)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_get_user(test_db):
    client.post("/users", json=DATA_USER)
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1


def test_read_main(test_db):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
