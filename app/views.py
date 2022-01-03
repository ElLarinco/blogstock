from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from . import db
from app.models import Post, User

views = Blueprint("views", __name__)

@views.route("/home")
@views.route("/")
def home_page():
    return render_template("home.html", user=current_user)

@views.route("/posts")
def posts_page():
    posts = Post.query.all()
    return render_template(
        "posts.html", 
        user=current_user, posts=posts)

@views.route("/users")
def users_page():
    users = User.query.all()
    return render_template(
        "users.html", user=current_user, users=users)

@views.route("/user_dashboard", methods=["GET", "POST"])
@login_required
def user_dashboard_page():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if len(content) < 1:
            flash("Enter some content...", category="error")
        else:
            new_post = Post(
                title=title,
                content=content,
                author_username=current_user.username
            )
            db.session.add(new_post)
            db.session.commit()
            flash("Post created", category="success")
            return redirect(url_for("views.posts_page"))

    return render_template("user_dashboard.html", user=current_user)