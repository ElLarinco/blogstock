from sqlalchemy.orm import relationship
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(255))
    posts = db.relationship('Post')

class Post(db.Model):
    id = db.Column(
        db.Integer, primary_key=True)
    title = db.Column(
        db.String(50))
    content = db.Column(
        db.String(10000))
    date = db.Column(
        db.DateTime(timezone=True), default=func.now())
    author_username = db.Column(
        db.String(150), db.ForeignKey('user.username')
    )