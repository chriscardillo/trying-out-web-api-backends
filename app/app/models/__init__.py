from app import db
from .mixins import *
from uuid import uuid4
from sqlalchemy import func
from .associations import *
from flask import current_app
from sqlalchemy.orm import column_property
from sqlalchemy.ext.hybrid import hybrid_property
from string import ascii_letters, digits, whitespace
from sqlalchemy.orm import validates, column_property
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


# ===== Models ===== #

class User(db.Model, StandardMixins):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email=db.Column(db.String(50), index=True, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    uuid=db.Column(db.String(32), nullable=False, default=uuid4().hex)
    todos = db.relationship('Todo', back_populates='user', lazy='subquery', cascade="all, delete-orphan")

    def searchable(value):
        return value.lower().replace(" ", "")

    @hybrid_property
    def _username(self):
        return func.lower(self.username)

    @validates('email')
    def convert_email(self, key, value):
        return value.lower().replace(" ", "")

    @validates('username')
    def convert_username(self, key, value):
        username = value.replace(" ", "")
        username_check = username.lower()
        user_check = User.query.filter(User._username == username_check).first()
        if user_check and user_check.id != self.id:
            raise AssertionError("Username or email already exists.")
        valid_username = ascii_letters + digits + '_'
        if set(username).difference(valid_username):
            raise AssertionError("Please use valid characters for usernames")
        else:
            return username

    @validates('password')
    def hash_password(self, key, value):
        return generate_password_hash(value, method='pbkdf2:sha512', salt_length=128)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in = current_app.config['TOKEN_EXPIRY'])
        new_uuid = uuid4().hex
        self.uuid = new_uuid
        db.session.commit()
        token_encoded = s.dumps({ 'id': self.id, 'hash': new_uuid })
        return token_encoded.decode('ascii')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        if user.uuid != data['hash']:
            user = None
        return user

class Todo(db.Model, StandardMixins):
    __tablename__ = 'todos'
    __table_args__ = {'extend_existing': True}
    title = db.Column(db.String(255), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user=db.relationship('User', back_populates='todos', lazy='subquery')
    tags=db.relationship('Tag', secondary=todo_tags, lazy='subquery',
                         backref='todos')

class Tag(db.Model, PrimaryKeyIdMixin, TimestampMixin):
    __tablename__ = 'tags'
    tag = db.Column(db.String(15), nullable=False)

    @validates('tag')
    def convert_tag(self, key, value):
        return value.strip()

    @hybrid_property
    def _tag(self):
        return func.trim(func.lower(self.tag))

    def searchable(value):
        return value.lower().strip()
