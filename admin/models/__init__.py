from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()


class Users(db.Model):
    __tablename__='users'

    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(250),nullable=False)
    password = db.Column(db.String(250),nullable=False)
    email = db.Column(db.String(250),nullable=False)
    def __init__(self,username, password, email):
        self.username = username
        self.password = password
        self.email = email

class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    user = db.relationship('Users', backref=db.backref('notes', lazy=True))

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id