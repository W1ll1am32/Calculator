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


def test_positive_operations_1():
    response = client.get("/add", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_positive_operations_2():
    response = client.get("/multiply", params={"a": 3, "b": -2})
    assert response.status_code == 200
    assert response.json()["result"] == -6


def test_positive_operations_3():
    response = client.get("/divide", params={"a": 7, "b": 2})
    assert response.status_code == 200
    assert response.json()["result"] == 3.5


def test_result_is_rounded():
    response = client.get("/divide", params={"a": 1, "b": 3})
    assert response.json()["result"] == round(1 / 3, app_final.PRECISION)


def test_divide_by_zero():
    response = client.get("/divide", params={"a": 1, "b": 0})
    assert response.status_code == 400


def test_unknown_operation():
    response = client.get("/something", params={"a": 2, "b": 3})
    assert response.status_code == 404


def test_missing_parameter():
    response = client.get("/add", params={"a": 1})
    assert response.status_code == 422


def test_not_a_number():
    response = client.get("/add", params={"a": "abc", "b": 1})
    assert response.status_code == 422
