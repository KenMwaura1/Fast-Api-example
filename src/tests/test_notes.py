"""
Comprehensive tests for the Notes API endpoints
"""

import pytest
from datetime import datetime
from app.api import crud


def get_iso_date():
    """Generate current ISO format date"""
    return datetime.now().isoformat()


class TestCreateNote:
    """Tests for creating notes"""

    def test_create_note_success(self, test_app, monkeypatch, test_user):
        """Test successful note creation"""
        test_request_payload = {
            "title": "something",
            "description": "something else",
            "completed": False,
            "tags": ["work"],
        }
        test_response_payload = {
            "id": 1,
            "title": "something",
            "description": "something else",
            "completed": False,
            "is_deleted": False,
            "tags": ["work"],
            "owner_id": test_user.id,
            "created_date": get_iso_date(),
        }

        async def mock_post(session, payload, owner_id):
            return 1

        async def mock_get(session, id):
            return test_response_payload

        monkeypatch.setattr(crud, "post", mock_post)
        monkeypatch.setattr(crud, "get", mock_get)

        response = test_app.post("/notes/", json=test_request_payload)
        assert response.status_code == 201
        assert response.json() == test_response_payload

    @pytest.mark.parametrize(
        "test_payload, expected_status",
        [
            ({}, 422),  # Missing required fields
            ({"description": "bar"}, 422),  # Missing title
            (
                {"title": "foo", "description": "bar", "completed": True, "tags": []},
                201,
            ),  # Valid
            ({"title": "1", "description": "bar"}, 422),  # Title too short
            ({"title": "foo", "description": "1"}, 422),  # Description too short
            ({"title": "x" * 256, "description": "bar"}, 422),  # Title too long
            ({"title": "foo", "description": "x" * 1001}, 422),  # Description too long
        ],
    )
    def test_create_note_validation(
        self, test_app, monkeypatch, test_user, test_payload, expected_status
    ):
        """Test note creation with invalid payloads"""

        async def mock_post(session, payload, owner_id):
            return 1

        async def mock_get(session, id):
            return {
                "id": 1,
                "title": test_payload.get("title", ""),
                "description": test_payload.get("description", ""),
                "completed": test_payload.get("completed", False),
                "is_deleted": False,
                "tags": test_payload.get("tags", []),
                "owner_id": test_user.id,
                "created_date": get_iso_date(),
            }

        monkeypatch.setattr(crud, "post", mock_post)
        monkeypatch.setattr(crud, "get", mock_get)

        response = test_app.post("/notes/", json=test_payload)
        assert response.status_code == expected_status


class TestReadNotes:
    """Tests for reading notes"""

    def test_read_single_note(self, test_app, monkeypatch, test_user):
        """Test reading a single note by ID"""
        test_data = {
            "title": "something",
            "description": "something else",
            "id": 1,
            "completed": False,
            "is_deleted": False,
            "tags": [],
            "owner_id": test_user.id,
            "created_date": get_iso_date(),
        }

        async def mock_get(session, id):
            return test_data

        monkeypatch.setattr(crud, "get", mock_get)

        response = test_app.get("/notes/1")
        assert response.status_code == 200
        assert response.json() == test_data

    def test_read_note_not_found(self, test_app, monkeypatch):
        """Test reading non-existent note returns 404"""

        async def mock_get(session, id):
            return None

        monkeypatch.setattr(crud, "get", mock_get)

        response = test_app.get("/notes/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_read_note_invalid_id(self, test_app, monkeypatch):
        """Test reading note with invalid ID"""
        response = test_app.get("/notes/0")
        assert response.status_code == 422

        response = test_app.get("/notes/invalid")
        assert response.status_code == 422

    def test_read_all_notes(self, test_app, monkeypatch, test_user):
        """Test reading all notes with default pagination"""
        test_data = [
            {
                "title": "note 1",
                "description": "desc 1",
                "id": 1,
                "completed": False,
                "is_deleted": False,
                "tags": ["work"],
                "owner_id": test_user.id,
                "created_date": get_iso_date(),
            },
            {
                "title": "note 2",
                "description": "desc 2",
                "id": 2,
                "completed": False,
                "is_deleted": False,
                "tags": [],
                "owner_id": test_user.id,
                "created_date": get_iso_date(),
            },
        ]

        async def mock_get_notes(
            session, owner_id, skip=0, limit=10, search=None, completed=None, tag=None
        ):
            return test_data

        monkeypatch.setattr(crud, "get_notes", mock_get_notes)

        response = test_app.get("/notes/")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json() == test_data

    def test_read_notes_with_pagination(self, test_app, monkeypatch, test_user):
        """Test note pagination with skip and limit"""
        test_data = [
            {
                "title": "note 1",
                "description": "desc 1",
                "id": 1,
                "completed": False,
                "is_deleted": False,
                "tags": [],
                "owner_id": test_user.id,
                "created_date": get_iso_date(),
            }
        ]

        async def mock_get_notes(
            session, owner_id, skip=0, limit=10, search=None, completed=None, tag=None
        ):
            return test_data if skip == 0 and limit == 1 else []

        monkeypatch.setattr(crud, "get_notes", mock_get_notes)

        response = test_app.get("/notes/?skip=0&limit=1")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_read_notes_pagination_invalid_limit(self, test_app, monkeypatch):
        """Test that limit exceeding maximum is rejected"""

        async def mock_get_notes(
            session, owner_id, skip=0, limit=10, search=None, completed=None, tag=None
        ):
            return []

        monkeypatch.setattr(crud, "get_notes", mock_get_notes)

        response = test_app.get("/notes/?limit=101")
        assert response.status_code == 422

    def test_read_notes_filter_by_completion(self, test_app, monkeypatch, test_user):
        """Test filtering notes by completion status"""
        completed_notes = [
            {
                "title": "note 1",
                "description": "desc 1",
                "id": 1,
                "completed": True,
                "is_deleted": False,
                "tags": [],
                "owner_id": test_user.id,
                "created_date": get_iso_date(),
            }
        ]

        async def mock_get_notes(
            session, owner_id, skip=0, limit=10, search=None, completed=None, tag=None
        ):
            if completed is True:
                return completed_notes
            return []

        monkeypatch.setattr(crud, "get_notes", mock_get_notes)

        response = test_app.get("/notes/?completed=true")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["completed"] is True

    def test_read_notes_search(self, test_app, monkeypatch, test_user):
        """Test searching notes by title/description"""
        search_results = [
            {
                "title": "unique title",
                "description": "desc 1",
                "id": 1,
                "completed": False,
                "is_deleted": False,
                "tags": [],
                "owner_id": test_user.id,
                "created_date": get_iso_date(),
            }
        ]

        async def mock_get_notes(
            session, owner_id, skip=0, limit=10, search=None, completed=None, tag=None
        ):
            if search and "unique" in search:
                return search_results
            return []

        monkeypatch.setattr(crud, "get_notes", mock_get_notes)

        response = test_app.get("/notes/?search=unique")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert "unique" in response.json()[0]["title"].lower()

    def test_read_notes_combined_filters(self, test_app, monkeypatch, test_user):
        """Test combining search and completion filters"""

        async def mock_get_notes(
            session, owner_id, skip=0, limit=10, search=None, completed=None, tag=None
        ):
            if search == "test" and completed is True:
                return [
                    {
                        "title": "test note",
                        "description": "desc",
                        "id": 1,
                        "completed": True,
                        "is_deleted": False,
                        "tags": [],
                        "owner_id": test_user.id,
                        "created_date": get_iso_date(),
                    }
                ]
            return []

        monkeypatch.setattr(crud, "get_notes", mock_get_notes)

        response = test_app.get("/notes/?search=test&completed=true")
        assert response.status_code == 200
        assert len(response.json()) == 1


class TestUpdateNote:
    """Tests for updating notes"""

    def test_update_note_success(self, test_app, monkeypatch, test_user):
        """Test successful note update"""
        test_update_data = {
            "title": "updated title",
            "description": "updated description",
            "completed": True,
            "tags": ["personal"],
        }
        test_response = {
            "id": 1,
            "title": "updated title",
            "description": "updated description",
            "completed": True,
            "is_deleted": False,
            "tags": ["personal"],
            "owner_id": test_user.id,
            "created_date": get_iso_date(),
        }

        async def mock_get(session, id):
            return test_response if id == 1 else None

        async def mock_put(session, id, payload):
            return 1

        monkeypatch.setattr(crud, "get", mock_get)
        monkeypatch.setattr(crud, "put", mock_put)

        response = test_app.put("/notes/1", json=test_update_data)
        assert response.status_code == 200
        assert response.json() == test_response

    def test_update_note_not_found(self, test_app, monkeypatch):
        """Test updating non-existent note returns 404"""

        async def mock_get(session, id):
            return None

        monkeypatch.setattr(crud, "get", mock_get)

        response = test_app.put(
            "/notes/999", json={"title": "foo", "description": "bar"}
        )
        assert response.status_code == 404

    @pytest.mark.parametrize(
        "id, payload, expected_status",
        [
            (1, {}, 422),  # Missing fields
            (1, {"description": "bar"}, 422),  # Missing title
            (999, {"title": "foo", "description": "bar"}, 404),  # Not found
            (1, {"title": "1", "description": "bar"}, 422),  # Title too short
            (1, {"title": "foo", "description": "1"}, 422),  # Description too short
            (0, {"title": "foo", "description": "bar"}, 422),  # Invalid ID
        ],
    )
    def test_update_note_validation(
        self, test_app, monkeypatch, test_user, id, payload, expected_status
    ):
        """Test note update with invalid data"""

        async def mock_get(session, note_id):
            return (
                None
                if note_id == 999 or note_id <= 0
                else {
                    "id": note_id,
                    "title": "existing",
                    "description": "existing",
                    "completed": False,
                    "is_deleted": False,
                    "tags": [],
                    "owner_id": test_user.id,
                    "created_date": get_iso_date(),
                }
            )

        monkeypatch.setattr(crud, "get", mock_get)

        response = test_app.put(f"/notes/{id}", json=payload)
        assert response.status_code == expected_status


class TestDeleteNote:
    """Tests for deleting notes"""

    def test_delete_note_success(self, test_app, monkeypatch, test_user):
        """Test successful note deletion"""
        test_data = {
            "title": "something",
            "description": "something else",
            "id": 1,
            "completed": False,
            "is_deleted": False,
            "tags": [],
            "owner_id": test_user.id,
            "created_date": get_iso_date(),
        }

        async def mock_get(session, id):
            return test_data if id == 1 else None

        async def mock_delete_note(session, id):
            return 1

        monkeypatch.setattr(crud, "get", mock_get)
        monkeypatch.setattr(crud, "delete_note", mock_delete_note)

        response = test_app.delete("/notes/1")
        assert response.status_code == 200
        assert response.json() == test_data

    def test_delete_note_not_found(self, test_app, monkeypatch):
        """Test deleting non-existent note returns 404"""

        async def mock_get(session, id):
            return None

        monkeypatch.setattr(crud, "get", mock_get)

        response = test_app.delete("/notes/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_delete_note_invalid_id(self, test_app, monkeypatch):
        """Test deleting with invalid ID"""
        response = test_app.delete("/notes/0")
        assert response.status_code == 422

        response = test_app.delete("/notes/invalid")
        assert response.status_code == 422

    def test_delete_note_already_deleted(self, test_app, monkeypatch):
        """Test that already soft-deleted note cannot be deleted again (regression)"""

        async def mock_get(session, id):
            return None

        async def mock_delete_note(session, id):
            return 0

        monkeypatch.setattr(crud, "get", mock_get)
        monkeypatch.setattr(crud, "delete_note", mock_delete_note)

        response = test_app.delete("/notes/1")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
