import os
from flask import Flask
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api_manager = APIManager(app, flask_sqlalchemy_db=db)
auth_manager = HTTPBasicAuth()

from app.site import bp as site_bp
from app.graphql import bp as graphql_bp
from app.restless import bp as restless_bp
from app.auth import bp as auth_bp

app.register_blueprint(site_bp, url_prefix='/site')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(graphql_bp, url_prefix='/api/graphql')
app.register_blueprint(restless_bp, url_prefix='/api/restless')

@app.route('/')
def index():
    return "Auth: a work in progress"
