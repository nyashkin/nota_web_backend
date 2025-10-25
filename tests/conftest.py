import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(__file__) + "/..")

from src.__main__ import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
