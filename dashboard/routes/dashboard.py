from flask import Blueprint, redirect, render_template, session, url_for

from dashboard.analytics import build_dashboard_data
from dashboard.security import login_required, verify_csrf

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    context = build_dashboard_data()
    context["username"] = session.get("username", "User")
    return render_template("dashboard.html", **context)


@dashboard_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    verify_csrf()
    session.clear()
    return redirect(url_for("home"))