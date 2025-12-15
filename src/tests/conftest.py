import pytest
from starlette.testclient import TestClient
from app.main import app
from app.db import database, metadata

@pytest.fixture(scope="module")
def test_app():
    # Mock database connection
    async def mock_connect():
        pass

    async def mock_disconnect():
        pass

    def mock_create_all(engine):
        pass

    database.connect = mock_connect
    database.disconnect = mock_disconnect
    metadata.create_all = mock_create_all

    with TestClient(app) as client:
        yield client
    