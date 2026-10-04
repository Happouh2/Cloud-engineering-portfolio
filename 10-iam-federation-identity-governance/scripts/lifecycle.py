import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE = "http://localhost:8080"
REALM = "portfolio"
ADMIN_USER = os.getenv("KEYCLOAK_ADMIN")
ADMIN_PASS = os.getenv("KEYCLOAK_ADMIN_PASSWORD")


def get_admin_token():
    r = requests.post(
        f"{BASE}/realms/master/protocol/openid-connect/token",
        data={"grant_type": "password", "client_id": "admin-cli",
              "username": ADMIN_USER, "password": ADMIN_PASS},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["access_token"]


def api(token):
    s = requests.Session()
    s.headers["Authorization"] = f"Bearer {token}"
    s.timeout = 15
    return s


def group_id(s, name):
    groups = s.get(f"{BASE}/admin/realms/{REALM}/groups").json()
    return next(g["id"] for g in groups if g["name"] == name)


def find_user(s, username):
    users = s.get(f"{BASE}/admin/realms/{REALM}/users", params={"username": username, "exact": "true"}).json()
    return users[0]["id"] if users else None


def onboard_joiner(s, username, group):
    existing = find_user(s, username)
    if existing:  # makes the script safe to re-run
        s.delete(f"{BASE}/admin/realms/{REALM}/users/{existing}").raise_for_status()
    r = s.post(f"{BASE}/admin/realms/{REALM}/users", json={"username": username, "enabled": True})
    r.raise_for_status()
    uid = r.headers["Location"].split("/")[-1]
    s.put(f"{BASE}/admin/realms/{REALM}/users/{uid}/groups/{group_id(s, group)}").raise_for_status()
    print(f"JOINER  {username} created in {group}")
    return uid


def move_user(s, uid, old_group, new_group):
    s.delete(f"{BASE}/admin/realms/{REALM}/users/{uid}/groups/{group_id(s, old_group)}").raise_for_status()
    s.put(f"{BASE}/admin/realms/{REALM}/users/{uid}/groups/{group_id(s, new_group)}").raise_for_status()
    print(f"MOVER   {uid} moved {old_group} -> {new_group}")


def offboard_leaver(s, uid):
    s.put(f"{BASE}/admin/realms/{REALM}/users/{uid}", json={"enabled": False}).raise_for_status()
    print(f"LEAVER  {uid} disabled")


def show(s, uid, label):
    groups = [g["name"] for g in s.get(f"{BASE}/admin/realms/{REALM}/users/{uid}/groups").json()]
    enabled = s.get(f"{BASE}/admin/realms/{REALM}/users/{uid}").json()["enabled"]
    print(f"  [{label}] groups={groups} enabled={enabled}")


if __name__ == "__main__":
    s = api(get_admin_token())
    uid = onboard_joiner(s, "jane.doe", "engineering")
    show(s, uid, "after joiner")
    move_user(s, uid, "engineering", "security")
    show(s, uid, "after mover")
    offboard_leaver(s, uid)
    show(s, uid, "after leaver")
