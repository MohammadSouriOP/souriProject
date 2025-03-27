import pytest
from fastapi.testclient import TestClient

from app import app  # import your FastAPI app instance directly


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client
