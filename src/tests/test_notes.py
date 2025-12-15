import json
import pytest
from datetime import datetime
from app.api import crud


def get_iso_date():
    return datetime.now().isoformat()


def test_create_note(test_app, monkeypatch):
    test_request_payload = {
        "title": "something",
        "description": "something else",
        "completed": False
    }
    test_response_payload = {
        "id": 1,
        "title": "something",
        "description": "something else",
        "completed": False,
        "created_date": get_iso_date()
    }

    async def mock_post(payload):
        return 1
    
    async def mock_get(id):
        return test_response_payload

    monkeypatch.setattr(crud, "post", mock_post)
    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.post("/notes/", content=json.dumps(test_request_payload))
    assert response.status_code == 201
    assert response.json() == test_response_payload


@pytest.mark.parametrize(
    "test_payload, expected_status",
    [
        [{}, 422],
        [{"description": "bar"}, 422],
        [{"title": "foo", "description": "bar", "completed": True}, 201],
        [{"title": "1", "description": "bar"}, 422],
        [{"title": "foo", "description": "1"}, 422]
    ]
)
def test_create_note_invalid(test_app, monkeypatch, test_payload, expected_status):
    async def mock_post(payload):
        return 1
    
    async def mock_get(id):
         return {
            "id": 1,
            "title": test_payload.get("title"),
            "description": test_payload.get("description"),
            "completed": test_payload.get("completed", False),
            "created_date": get_iso_date()
        }

    monkeypatch.setattr(crud, "post", mock_post)
    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.post("/notes/", content=json.dumps(test_payload))
    assert response.status_code == expected_status


def test_read_note(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1, "completed": False,
                 "created_date": get_iso_date()}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.get("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.get("/notes/0/")
    assert response.status_code == 422


def test_read_notes_pagination(test_app, monkeypatch):
    test_data = [
        {"title": "note 1", "description": "desc 1", "id": 1, "completed": False, "created_date": get_iso_date()},
        {"title": "note 2", "description": "desc 2", "id": 2, "completed": False, "created_date": get_iso_date()}
    ]

    async def mock_get_notes(skip=0, limit=10, search=None, completed=None):
        return test_data

    monkeypatch.setattr(crud, "get_notes", mock_get_notes)

    response = test_app.get("/notes/?skip=0&limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == test_data


def test_read_notes_filter(test_app, monkeypatch):
    test_data = [
        {"title": "note 1", "description": "desc 1", "id": 1, "completed": True, "created_date": get_iso_date()}
    ]

    async def mock_get_notes(skip=0, limit=10, search=None, completed=None):
        if completed:
            return test_data
        return []

    monkeypatch.setattr(crud, "get_notes", mock_get_notes)

    response = test_app.get("/notes/?completed=true")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["completed"] is True


def test_read_notes_search(test_app, monkeypatch):
    test_data = [
        {"title": "unique", "description": "desc 1", "id": 1, "completed": False, "created_date": get_iso_date()}
    ]

    async def mock_get_notes(skip=0, limit=10, search=None, completed=None):
        if search == "unique":
            return test_data
        return []

    monkeypatch.setattr(crud, "get_notes", mock_get_notes)

    response = test_app.get("/notes/?search=unique")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "unique"


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"description": "bar"}, 422],
        [999, {"title": "foo", "description": "bar", "completed": True}, 404],
        [1, {"title": "1", "description": "bar"}, 422],
        [1, {"title": "foo", "description": "1"}, 422],
        [0, {"title": "foo", "description": "bar"}, 422],
    ],
)
def test_update_note_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        if id == 999: return None
        return {"id": id, "title": "existing", "description": "existing", "completed": False, "created_date": get_iso_date()}

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.put(f"/notes/{id}/", content=json.dumps(payload))
    assert response.status_code == status_code


def test_remove_note_200(test_app, monkeypatch):
    test_data = {"title": "something", "description": "something else", "id": 1, "completed": False,
                 "created_date": get_iso_date()}

    async def mock_get(id):
        return test_data

    async def mock_delete(id):
        return id

    monkeypatch.setattr(crud, "get", mock_get)
    monkeypatch.setattr(crud, "delete", mock_delete)

    response = test_app.delete("/notes/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_note_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(crud, "get", mock_get)

    response = test_app.delete("/notes/999/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Note not found"

    response = test_app.delete("/notes/0/")
    assert response.status_code == 422


def test_remove_note_invalid_id(test_app, monkeypatch):
    response = test_app.delete("/notes/one/")
    assert response.status_code == 422

