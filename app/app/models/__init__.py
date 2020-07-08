from app import app, db
from datetime import datetime
from sqlalchemy.orm import validates, column_property
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

# ===== Mixins ===== #

class PrimaryKeyIdMixin:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ===== Models ===== #

class User(db.Model, PrimaryKeyIdMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    email=db.Column(db.String(50), index=True, unique=True, nullable=False)
    password=db.Column(db.String, nullable=False)
    todos = db.relationship('Todo', back_populates='user', lazy='subquery')

    @validates('email')
    def convert_email(self, key, value):
        return value.lower().replace(" ", "")

    # Users shoudl be able to have a username that is case-insensitive!
    # Figure out how to validate username properly
    @validates('username')
    def convert_username(self, key, value):
        return value.lower().replace(" ", "")

    @validates('password')
    def hash_password(self, key, value):
        return generate_password_hash(value, method='pbkdf2:sha512')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    #expiration should be configurable
    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'], expires_in = app.config['TOKEN_EXPIRY'])
        return s.dumps({ 'id': self.id, 'hash': self.password }) # is it okay to put a hashed password in the token?

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        # Hash in token must match user password
        if user.password != data['hash']:
            user = None
        return user

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
