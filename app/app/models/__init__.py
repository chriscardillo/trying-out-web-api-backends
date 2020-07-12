from app import db
from uuid import uuid4
from flask import current_app
from .mixins import PrimaryKeyIdMixin, StandardMixins
from sqlalchemy.orm import validates, column_property
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


# ===== Models ===== #

class User(db.Model, StandardMixins):
    __tablename__ = 'users'
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email=db.Column(db.String(50), index=True, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    uuid=db.Column(db.String(36), nullable=False, default=uuid4().hex)
    todos = db.relationship('Todo', back_populates='user', lazy='subquery', cascade="all, delete-orphan")

    @validates('email')
    def convert_email(self, key, value):
        return value.lower().replace(" ", "")

    # Users should be able to have a username that is case-insensitive!
    # Figure out how to validate username properly
    @validates('username')
    def convert_username(self, key, value):
        return value.lower().replace(" ", "")

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
        return s.dumps({ 'id': self.id, 'hash': new_uuid })

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
    title = db.Column(db.String(255), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user=db.relationship('User', back_populates='todos', lazy='subquery')

class Manufacturer(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'manufacturers'
    manufacturer = db.Column(db.String, index=True, unique=True, nullable=False)

    @validates('manufacturer')
    def convert_lower(self, key, value):
        return value.lower()
