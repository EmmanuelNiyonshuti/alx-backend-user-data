#!/usr/bin/env python3
""" query and tests endpoints """
import requests


def register_user(email: str, password: str) -> None:
    """ query users endpoint to register a new user."""
    data = {"email": email, "password": password}
    resp = requests.post("http://127.0.0.1:5000/users", data=data)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    query sessions endpoint with wrong credentials.
    """
    data = {"email": email, "password": password}
    resp = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """ query session endpoint with valid credentials."""
    data = {"email": email, "password": password}
    resp = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload == {"email": email, "message": "logged in"}


def profile_unlogged() -> None:
    """ query profile endpoint when logged out """
    resp = requests.get("http://127.0.0.1:5000/profile")
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """ query profile endpoint when logged out  """
    cookies = {"session_id": session_id}
    resp = requests.get("http://127.0.0.1:5000/profile", cookies=cookies)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload == {"email": user.email}


def log_out(session_id: str) -> None:
    """ query sessions endpoint to logout a user """
    cookies = {"session_id": session_id}
    resp = requests.get("http://127.0.0.1:5000/sessions", cookies=cookies)
    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """ query reset_password endpoint set password token"""
    data = {"email": email}
    resp = requests.post("http://127.0.0.1:5000/reset_password", data=data)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload == {"email": email, "reset_token": reset_token}


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ query  reset_password endpoint to update password. """
    data = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    resp = requests.put("http://127.0.0.1:5000/reset_password", data=data)
    assert resp.status_code == 200
    payload = resp.json()
    assert payload == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
