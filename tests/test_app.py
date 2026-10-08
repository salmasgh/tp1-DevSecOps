import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402

import main  # noqa: E402

client = TestClient(main.app)


def test_register_then_get_user():
    r = client.post("/register", params={"name": "alice", "password": "pw123"})
    assert r.status_code == 200
    r = client.get("/user", params={"name": "alice"})
    assert r.status_code == 200
    assert any(u["name"] == "alice" for u in r.json()["users"])


def test_ping_localhost():
    r = client.get("/ping", params={"host": "127.0.0.1"})
    assert r.status_code == 200
    assert "returncode" in r.json()
