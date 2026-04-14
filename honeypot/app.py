from flask import Flask, render_template
from common.db import initDb
from .routes.login import loginBp
from .routes.signup import signupBp

app = Flask(__name__)
initDb()
app.register_blueprint(loginBp)
app.register_blueprint(signupBp)

@app.route('/')
def index():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    