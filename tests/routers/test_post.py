from tests.conftest import client, test_db

POST_DATA = {"content": "string"}
FIND_POST_DATA = {
    "filters": {
        "id": 1,
        "content": "string",
    },
    "group": {
        "group_by": "asc",
        "sort_by": "publication_date"
    }
    }


def test_create_post(test_db):
    response = client.post("/post", json=POST_DATA)
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "string"
    assert data["id"] == 1


def test_ifo_about_post(test_db):
    client.post("/post", json=POST_DATA)
    response = client.get("/post/1")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "string"
    assert data["id"] == 1


def test_change_post(test_db):
    client.post("/post", json=POST_DATA)
    response = client.put("/post/1/?new_content=new_string")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "new_string"
    assert data["id"] == 1


def test_delete_post(test_db):
    client.post("/post", json=POST_DATA)
    response = client.delete("/post/1")
    assert response.status_code == 200


def test_find_post(test_db):
    client.post("/post", json=POST_DATA)
    response = client.post("/find_post", json=FIND_POST_DATA)
    assert response.status_code == 200


def test_like_post(test_db):
    client.post("/post", json=POST_DATA)
    response = client.get("/like/?id=1")
    assert response.status_code == 200
    assert response.json() == {'message': 'You like it'}
    response = client.get("/like/?id=1")
    assert response.status_code == 200
    assert response.json() == {'message': 'You delete like'}
    response = client.get("/like/?id=2")
    assert response.status_code == 403
    assert response.json() == {'detail': 'You cannot like this post'}
