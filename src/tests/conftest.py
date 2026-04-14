import pytest
from starlette.testclient import TestClient
from unittest.mock import AsyncMock
from contextlib import asynccontextmanager

from app.main import app
from app.api.models import UserDB
from datetime import datetime


@asynccontextmanager
async def mock_lifespan(app):
    yield


@pytest.fixture(scope="module")
def test_app():
    # Disable actual database connection in lifespan
    app.router.lifespan_context = mock_lifespan

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="module")
def test_user():
    return UserDB(
        id=1,
        username="testuser",
        email="test@example.com",
        is_active=True,
        created_date=datetime.now(),
    )


@pytest.fixture(scope="module")
def token_headers(test_user):
    # In a real scenario, we'd generate a real token
    # For mocking, we'll just provide a dummy header and rely on dependency override
    return {"Authorization": "Bearer dummy-token"}


@pytest.fixture(autouse=True)
def override_auth_dependencies(test_user):
    from app.api.dependencies import get_current_active_user, get_db

    async def override_get_db():
        yield AsyncMock()

    async def override_get_current_user():
        return test_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_active_user] = override_get_current_user

    yield

    app.dependency_overrides = {}
