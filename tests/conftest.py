from fastapi.testclient import TestClient
import pytest
import sys
import os

sys.path.append(os.path.dirname(__file__) + "/..")

from src.__main__ import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
