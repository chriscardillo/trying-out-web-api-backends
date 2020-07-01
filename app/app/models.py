from app import db
from datetime import datetime
from sqlalchemy.orm import validates

# ===== Mixins ===== #

class PrimaryKeyIdMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

# ===== Models ===== #

class User(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(255), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    todos = db.relationship('Todo', back_populates='user', lazy='subquery')

    @validates('username', 'email')
    def convert_lower(self, key, value):
        return value.lower()

class Todo(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'todos'
    title = db.Column(db.String(255), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user=db.relationship('User', back_populates='todos', lazy='subquery')
    todo_items=db.relationship('TodoItem', back_populates='todo')

class TodoItem(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'todo_items'
    description = db.Column(db.String)
    is_done = db.Column(db.Boolean)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'), nullable=False)
    todo = db.relationship('Todo', back_populates='todo_items', lazy="subquery")
