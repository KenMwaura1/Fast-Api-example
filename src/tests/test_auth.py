from app.api import crud, security


class TestAuth:
    def test_register_user_success(self, test_app, monkeypatch):
        test_payload = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
        }
        test_response = {
            "id": 1,
            "username": "newuser",
            "email": "new@example.com",
            "is_active": True,
            "created_date": "2024-01-01T00:00:00",
        }

        # Mock user not existing initially
        async def mock_get_username(session, username):
            if username == "newuser":
                if not hasattr(mock_get_username, "called"):
                    mock_get_username.called = True
                    return None
                return test_response
            return None

        async def mock_get_email(session, email):
            return None

        async def mock_create_user(session, payload, hashed_password):
            return 1

        monkeypatch.setattr(crud, "get_user_by_username", mock_get_username)
        monkeypatch.setattr(crud, "get_user_by_email", mock_get_email)
        monkeypatch.setattr(crud, "create_user", mock_create_user)

        response = test_app.post("/auth/register", json=test_payload)
        assert response.status_code == 201
        assert response.json() == test_response

    def test_register_user_already_exists(self, test_app, monkeypatch):
        test_payload = {
            "username": "existing",
            "email": "existing@example.com",
            "password": "password123",
        }

        async def mock_get_username(session, username):
            return {"id": 1, "username": "existing"}

        monkeypatch.setattr(crud, "get_user_by_username", mock_get_username)

        response = test_app.post("/auth/register", json=test_payload)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_login_success(self, test_app, monkeypatch):
        test_user_data = {
            "id": 1,
            "username": "testuser",
            "hashed_password": security.get_password_hash("password123"),
        }

        async def mock_get_user(session, username):
            return test_user_data

        monkeypatch.setattr(crud, "get_user_by_username", mock_get_user)

        response = test_app.post(
            "/auth/token", data={"username": "testuser", "password": "password123"}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    def test_login_invalid_credentials(self, test_app, monkeypatch):
        async def mock_get_user(session, username):
            return None

        monkeypatch.setattr(crud, "get_user_by_username", mock_get_user)

        response = test_app.post(
            "/auth/token", data={"username": "wrong", "password": "wrong"}
        )
        assert response.status_code == 401
