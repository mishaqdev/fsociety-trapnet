from flask import Blueprint, render_template, request
from common.db import insertAttack

signupBp = Blueprint('signup', __name__)

@signupBp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')
        ip = request.remote_addr
        userAgent = request.headers.get('User-Agent')

        attackData = {
            "ip": ip,
            "requestPath": "/signup",
            "username": username,
            "password": password,
            "user_agent": userAgent,
            "status": "failed"
        }
        insertAttack(attackData)

        return render_template("signup.html", error="Signup is currently unavailable. Please try again later.")

    return render_template("signup.html")
