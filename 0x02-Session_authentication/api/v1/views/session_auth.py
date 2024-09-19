#!/usr/bin/env python3
""" session authentication view"""
from flask import request, jsonify
import os
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth():
    """
    POST /api/v1/auth_session/login
    return:
        user along with a session cookie.
    """
    email = request.form.get("email")
    if email is None:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if password is None:
        return jsonify({"error": "password missing"}), 400
    attributes = {"email": email, "password": password}
    user = User.search(attributes)
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    session_name = os.getenv("SESSION_NAME")
    user = user.to_json()
    user.set_cookie(session_name, session_id)
    return user
