#!/usr/bin/env python3
""" session authentication view"""
from flask import request, jsonify, make_response
import os
from api.v1.views import app_views
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def auth():
    """
    POST /api/v1/auth_session/login
    Return:
        user along with a session cookie.
    """
    user_email = request.form.get("email")
    if user_email is None or len(user_email) == 0:
        return jsonify({"error": "email missing"}), 400
    user_password = request.form.get("password")
    if user_password is None or len(user_password) == 0:
        return jsonify({"error": "password missing"}), 400
    attributes = {"email": user_email}
    users = User.search(attributes)
    if len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]
    if not user.is_valid_password(user_password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    cookie_name = os.getenv("SESSION_NAME")
    response.set_cookie(cookie_name, session_id)
    return response


@app_views.route("/auth_session/logout", methods=["DELETE"],
                 strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout.
    Return:
        empty dictionary when a user session is deleted.
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    auth.destroy_session(request)
    return jsonify({}), 200
