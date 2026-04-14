import re
import sqlite3

from flask import Blueprint, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from dashboard.db import create_user
from dashboard.security import verify_csrf

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]+$")

signup_bp = Blueprint("signup", __name__)


def valid_signup_payload(username: str, email: str, password: str) -> tuple[bool, str]:
    if not username or len(username) < 3 or len(username) > 32:
        return False, "Username must be 3-32 characters."
    if not USERNAME_RE.match(username):
        return False, "Username can contain letters, numbers and underscore only."
    if not email or not EMAIL_RE.match(email):
        return False, "Enter a valid email address."
    if not password or len(password) < 10:
        return False, "Password must be at least 10 characters."
    return True, ""


@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        verify_csrf()
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        valid, message = valid_signup_payload(username, email, password)
        if not valid:
            return render_template("signup.html", error=message), 400

        try:
            create_user(username, email, generate_password_hash(password))
        except sqlite3.IntegrityError:
            return render_template("signup.html", error="Username or email is already registered."), 409

        return redirect(url_for("login.login"))

    return render_template("signup.html")