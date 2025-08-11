import pytest
from fastapi.testclient import TestClient
from main import app
import uuid
import re

@pytest.fixture(scope="module")
def test_client():
    client = TestClient(app)
    yield client


def test_create_todo(test_client):
    payload = {"title": "Test Todo"}
    response = test_client.post("/todos", json=payload)
    data = response.json()

    try:
        assert response.status_code == 200 or response.status_code == 201
        assert "id" in data and isinstance(data["id"], str)
        assert data["title"] == "Test Todo"
        assert data["completed"] is False
    finally:
        test_create_todo.todo_id = data["id"]


def test_create_todo_malformed_payload(test_client):
    payload = {"completed": False}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 422

    payload = {"title": 123}
    response = test_client.post("/todos", json=payload)
    assert response.status_code == 422


def test_get_todos(test_client):
    response = test_client.get("/todos")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        todo = data[0]
        assert "id" in todo
        assert "title" in todo
        assert "completed" in todo
        assert "created_at" in todo
        assert "updated_at" in todo


def test_create_todo_with_extra_fields(test_client):
    payload = {"title": "Extra Fields", "extra": "should be ignored"}
    response = test_client.post("/todos", json=payload)
    data = response.json()
    try:
        assert response.status_code in (200, 201)
        assert "id" in data and "title" in data and "completed" in data
        assert data["title"] == "Extra Fields"
    finally:
        test_client.delete(f"/todos/{data['id']}")


def test_update_todo(test_client):
    todo_id = getattr(test_create_todo, "todo_id", None)
    assert todo_id is not None, "No todo_id from create test"
    payload = {"title": "Updated Todo", "completed": True}
    response = test_client.put(f"/todos/{todo_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated Todo"
    assert data["completed"] is True
    assert "updated_at" in data


def test_update_todo_partial_fields(test_client):
    payload = {"title": "Partial Update Todo"}
    response = test_client.post("/todos", json=payload)
    todo_id = response.json()["id"]

    try:
        assert response.status_code in (200, 201)
        payload = {"title": "Title Only Update"}
        r = test_client.put(f"/todos/{todo_id}", json=payload)
        assert r.status_code == 200
        assert r.json()["title"] == "Title Only Update"

        payload = {"completed": True}
        r = test_client.put(f"/todos/{todo_id}", json=payload)
        assert r.status_code == 200
        assert r.json()["completed"] is True
    finally:
        test_client.delete(f"/todos/{todo_id}")


def test_delete_todo(test_client):
    todo_id = getattr(test_create_todo, "todo_id", None)
    assert todo_id is not None, "No todo_id from create test"
    response = test_client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo deleted successfully"}


def test_delete_unknown_todo(test_client):
    unknown_id = str(uuid.uuid4())
    response = test_client.delete(f"/todos/{unknown_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_nonexistent_todo(test_client):
    unknown_id = str(uuid.uuid4())
    payload = {"title": "Doesn't exist", "completed": False}
    response = test_client.put(f"/todos/{unknown_id}", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"


def test_update_todo_malformed_payload(test_client):
    payload = {"title": "To be malformed"}
    response = test_client.post("/todos", json=payload)
    todo_id = response.json()["id"]

    try:
        r = test_client.put(f"/todos/{todo_id}", json={})
        assert r.status_code == 422

        r = test_client.put(f"/todos/{todo_id}", json={"title": 123, "completed": "nope"})
        assert r.status_code == 422
    finally:
        test_client.delete(f"/todos/{todo_id}")


def test_create_multiple_todos_and_list(test_client):
    ids = []
    try:
        for i in range(3):
            payload = {"title": f"Bulk {i}"}
            r = test_client.post("/todos", json=payload)
            ids.append(r.json()["id"])
        r = test_client.get("/todos")
        assert r.status_code == 200
        titles = [todo["title"] for todo in r.json()]
        for i in range(3):
            assert f"Bulk {i}" in titles
    finally:
        for id_ in ids:
            test_client.delete(f"/todos/{id_}")


def test_delete_todo_twice(test_client):
    payload = {"title": "Delete Twice"}
    r = test_client.post("/todos", json=payload)
    todo_id = r.json()["id"]

    try:
        r = test_client.delete(f"/todos/{todo_id}")
        assert r.status_code == 200
        r = test_client.delete(f"/todos/{todo_id}")
        assert r.status_code == 404
    finally:
        test_client.delete(f"/todos/{todo_id}")


def test_timestamps_format(test_client):
    payload = {"title": "Check Timestamp"}
    r = test_client.post("/todos", json=payload)
    todo_id = r.json()["id"]

    try:
        r = test_client.get("/todos")
        todo = next(t for t in r.json() if t["id"] == todo_id)
        pattern_iso_utc = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}[+-]\d{2}:\d{2}$"
        print(todo["created_at"])
        assert re.match(pattern_iso_utc, todo["created_at"])
        assert re.match(pattern_iso_utc, todo["updated_at"])
    finally:
        test_client.delete(f"/todos/{todo_id}")


def test_update_todo_no_fields(test_client):
    payload = {"title": "No fields update"}
    r = test_client.post("/todos", json=payload)
    todo_id = r.json()["id"]

    try:
        r = test_client.put(f"/todos/{todo_id}", json={})
        assert r.status_code == 422
    finally:
        test_client.delete(f"/todos/{todo_id}")


def test_create_todo_empty_title(test_client):
    payload = {"title": ""}
    r = test_client.post("/todos", json=payload)
    if r.status_code in (200, 201):
        todo_id = r.json()["id"]
        try:
            assert r.status_code in (200, 201, 422)
        finally:
            test_client.delete(f"/todos/{todo_id}")
    else:
        assert r.status_code == 422


def test_case_sensitivity_in_title(test_client):
    payload1 = {"title": "CaseTest"}
    payload2 = {"title": "casetest"}
    r1 = test_client.post("/todos", json=payload1)
    r2 = test_client.post("/todos", json=payload2)
    id1 = r1.json()["id"]
    id2 = r2.json()["id"]

    try:
        assert r1.status_code in (200, 201)
        assert r2.status_code in (200, 201)
        assert id1 != id2
    finally:
        test_client.delete(f"/todos/{id1}")
        test_client.delete(f"/todos/{id2}")
