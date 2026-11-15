# Shared setup for the tests: a pretend database, so no real Postgres or Redis is needed.
import os
from unittest import mock

import pytest

# app.py reads these two settings when it loads. Fake values are fine, nothing connects.
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")

# app.py talks to the database the moment it loads, so swap in a fake connect first.
with mock.patch("psycopg.connect"):
    import app as items_api


@pytest.fixture
def client():
    return items_api.app.test_client()


@pytest.fixture
def fake_db():
    # Every psycopg.connect() during one test returns this pretend connection.
    with mock.patch("psycopg.connect") as connect:
        yield connect.return_value.__enter__.return_value
