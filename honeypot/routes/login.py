from flask import Blueprint, render_template, request
from common.db import insertAttack

loginBp = Blueprint('login', __name__)

@loginBp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        ip = request.remote_addr
        userAgent = request.headers.get('User-Agent')

        attackData = {
            "ip": ip,
            "requestPath": "/login",
            "username": username,
            "password": password,
            "user_agent": userAgent,
            "status": "failed"
        }

        insertAttack(attackData)

        return render_template("login.html", error="Invalid credentials")

    # GET request → show login page
    return render_template("login.html")
