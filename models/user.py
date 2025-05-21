from database import db
from flask_login import UserMixin
# This is a simple user model for a Flask application using SQLAlchemy and Flask-Login.
# It defines a User class that inherits from db.Model and UserMixin.
# The User class has three fields: id, username, and password.

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)