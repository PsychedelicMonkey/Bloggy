from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    middle_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(164), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)