import json
import logging
import os
import time

import psycopg
import redis
from flask import Flask, Response, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("items-api")

DATABASE_URL = os.environ["DATABASE_URL"]
cache = redis.Redis.from_url(os.environ["REDIS_URL"], socket_timeout=1, socket_connect_timeout=1)
REQUESTS = Counter("http_requests_total", "HTTP requests", ["path", "status"])
app = Flask(__name__)


def db():
    return psycopg.connect(DATABASE_URL, connect_timeout=3)


def init_db():
    for attempt in range(10):
        try:
            with db() as conn:
                conn.execute("CREATE TABLE IF NOT EXISTS items (id SERIAL PRIMARY KEY, name TEXT NOT NULL)")
            log.info("database ready")
            return
        except psycopg.Error as exc:
            log.warning("database not ready (try %s): %s", attempt + 1, exc)
            time.sleep(2)
    raise RuntimeError("database never became ready")


init_db()


@app.after_request
def count(resp):
    path = request.url_rule.rule if request.url_rule else "unmatched"
    if path != "/metrics":
        REQUESTS.labels(path, resp.status_code).inc()
    return resp


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/ready")
def ready():
    try:
        with db() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ready")
    except psycopg.Error:
        return jsonify(status="database unavailable"), 503


@app.post("/items")
def add_item():
    name = (request.get_json(silent=True) or {}).get("name")
    if not name:
        return jsonify(error="name required"), 400
    with db() as conn:
        new_id = conn.execute("INSERT INTO items (name) VALUES (%s) RETURNING id", (name,)).fetchone()[0]
    try:
        cache.delete("items")
    except redis.RedisError:
        log.warning("cache unavailable, skipped clearing it")
    return jsonify(id=new_id, name=name), 201


@app.get("/items")
def list_items():
    try:
        saved = cache.get("items")
        if saved:
            return Response(saved, mimetype="application/json", headers={"X-Cache": "hit"})
    except redis.RedisError:
        log.warning("cache unavailable, reading the database")
    with db() as conn:
        rows = conn.execute("SELECT id, name FROM items ORDER BY id DESC LIMIT 100").fetchall()
    body = json.dumps([{"id": r[0], "name": r[1]} for r in rows])
    try:
        cache.setex("items", 10, body)
    except redis.RedisError:
        pass
    return Response(body, mimetype="application/json", headers={"X-Cache": "miss"})


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
