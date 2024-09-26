#!/usr/bin/env python3
"""
Basic flask app.
"""
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """ creates a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

@app.route("/sessions", methods=["POST"])
def login():
    """login a user."""
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    resp = make_response({"email": email, "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
