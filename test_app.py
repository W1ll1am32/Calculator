import pytest
from fastapi.testclient import TestClient

import app_final

client = TestClient(app_final.app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert response.json()["version"] == app_final.APP_VERSION
