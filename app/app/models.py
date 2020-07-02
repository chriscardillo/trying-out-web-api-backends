from app import db
from datetime import datetime
from sqlalchemy.orm import validates

# ===== Mixins ===== #

class PrimaryKeyIdMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ===== Models ===== #

class User(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    todos = db.relationship('Todo', back_populates='user', lazy='subquery')

    @validates('username', 'email')
    def convert_lower(self, key, value):
        return value.lower()

class Todo(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'todos'
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user=db.relationship('User', back_populates='todos', lazy='subquery')

class Manufacturer(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'manufacturers'
    manufacturer = db.Column(db.String, index=True, nullable=False)

    @validates('manufacturer')
    def convert_lower(self, key, value):
        return value.lower()
