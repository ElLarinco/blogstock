from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged succesfully", category="success")
                
                login_user(user, remember=True)

                return redirect(url_for("views.user_dashboard_page"))
            else:
                flash("Incorrect username or password", category="error")

        else:
            flash("Email does not exist", category="error")
                
    return render_template("login.html", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmPassword")

        user = User.query.filter_by(username=username).first()

        if user:
            flash("Username already exists", category="error")

        elif len(email) < 4:
            flash("Email must be greater than 4 characters", category='error')

        elif len(username) < 2:
            flash("Username must be greater than 2 characters", category='error')

        elif password != confirmPassword:
            flash("Passwords don\'t match", category='error')
            
        elif len(password) < 8:
            flash("Password must be at least 7 characters", category='error')

        else:
            new_user = User(
                username=username, 
                email=email, 
                password = generate_password_hash(password, method="sha256"))
            
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash("Account created", category="success")

            return redirect(url_for("views.posts_page"))

    return render_template("register.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_page"))