# Small, fast checks of the items API. Each test is one question with one right answer.
from unittest import mock

import psycopg
import redis

import app as items_api  # already loaded by conftest.py with the fake database


def test_health_says_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_ready_is_503_when_database_is_down(client):
    with mock.patch("psycopg.connect", side_effect=psycopg.OperationalError("db down")):
        resp = client.get("/ready")
    assert resp.status_code == 503


def test_add_item_needs_a_name(client):
    resp = client.post("/items", json={})
    assert resp.status_code == 400
    assert resp.get_json() == {"error": "name required"}


def test_add_item_saves_and_returns_it(client, fake_db):
    fake_db.execute.return_value.fetchone.return_value = (7,)
    with mock.patch.object(items_api.cache, "delete"):
        resp = client.post("/items", json={"name": "charlie"})
    assert resp.status_code == 201
    assert resp.get_json() == {"id": 7, "name": "charlie"}


def test_items_come_from_cache_when_saved(client):
    with mock.patch.object(items_api.cache, "get", return_value=b'[{"id": 1, "name": "alpha"}]'):
        resp = client.get("/items")
    assert resp.headers["X-Cache"] == "hit"
    assert resp.get_json() == [{"id": 1, "name": "alpha"}]


def test_items_still_work_when_cache_is_down(client, fake_db):
    fake_db.execute.return_value.fetchall.return_value = [(2, "bravo"), (1, "alpha")]
    with mock.patch.object(items_api.cache, "get", side_effect=redis.ConnectionError("no redis")), \
         mock.patch.object(items_api.cache, "setex", side_effect=redis.ConnectionError("no redis")):
        resp = client.get("/items")
    assert resp.status_code == 200
    assert resp.headers["X-Cache"] == "miss"
    assert resp.get_json() == [{"id": 2, "name": "bravo"}, {"id": 1, "name": "alpha"}]


def test_metrics_page_counts_requests(client):
    client.get("/health")
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"http_requests_total" in resp.data
