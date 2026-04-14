import os
import secrets

from flask import Flask, render_template

from dashboard.auth.login import login_bp
from dashboard.auth.signup import signup_bp
from dashboard.db import close_db, init_db
from dashboard.routes.dashboard import dashboard_bp
from dashboard.security import inject_csrf_token, set_security_headers

app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("DASHBOARD_SECRET_KEY", secrets.token_hex(32)),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
)

app.after_request(set_security_headers)
app.context_processor(inject_csrf_token)
app.teardown_appcontext(close_db)

app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(dashboard_bp)


@app.route("/")
def home():
    return render_template("home.html")


init_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
