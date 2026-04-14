import secrets

from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from dashboard.db import get_user_by_email
from dashboard.security import verify_csrf

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        verify_csrf()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = get_user_by_email(email)
        if not user or not check_password_hash(user["password_hash"], password):
            return render_template("login.html", error="Invalid email or password."), 401

        session.clear()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["csrf_token"] = secrets.token_urlsafe(32)
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")