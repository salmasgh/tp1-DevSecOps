"""Application VOLONTAIREMENT VULNERABLE - cible de scan pour un TP de securite.
NE JAMAIS DEPLOYER."""
import hashlib
import sqlite3
import subprocess

import requests
import yaml
from fastapi import FastAPI

# VULN: secret en dur dans le code source (Bandit B105)
SECRET_KEY = "super-secret-key-12345"

DB_PATH = "app.db"

app = FastAPI()


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "name TEXT NOT NULL, "
        "password TEXT NOT NULL)"
    )
    return conn


@app.get("/user")
def get_user(name: str):
    conn = get_db()
    # VULN: injection SQL via f-string (Bandit B608)
    query = f"SELECT id, name FROM users WHERE name = '{name}'"
    rows = conn.execute(query).fetchall()
    conn.close()
    return {"users": [{"id": r[0], "name": r[1]} for r in rows]}


@app.get("/ping")
def ping(host: str):
    # VULN: injection de commande via subprocess shell=True (Bandit B602)
    result = subprocess.run(
        f"ping -c 1 {host}", shell=True, capture_output=True, text=True
    )
    return {"returncode": result.returncode, "output": result.stdout}


@app.post("/register")
def register(name: str, password: str):
    # VULN: mot de passe hache avec MD5, algorithme faible (Bandit B324)
    hashed = hashlib.md5(password.encode()).hexdigest()
    conn = get_db()
    conn.execute(
        "INSERT INTO users (name, password) VALUES (?, ?)", (name, hashed)
    )
    conn.commit()
    conn.close()
    return {"status": "registered", "name": name}


@app.post("/config")
def load_config(data: str):
    # VULN: deserialisation dangereuse avec yaml.Loader (Bandit B506)
    config = yaml.load(data, Loader=yaml.Loader)
    return {"config": config}


@app.get("/fetch")
def fetch(url: str):
    # VULN: verification du certificat TLS desactivee (Bandit B501)
    r = requests.get(url, verify=False, timeout=5)
    return {"status_code": r.status_code, "body": r.text[:500]}
