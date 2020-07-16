import os
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import configs

db = SQLAlchemy()
migrate = Migrate()

def create_app(config=None):
    app = Flask(__name__)
    if config is None:
        config = os.environ.get('APP_CONFIG') or 'development'
    assert config in configs.keys(), "Please pick a valid config from: {}".format(", ".join(list(configs.keys())))
    app.config.from_object(configs[config])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.graphql import bp as graphql_bp
    app.register_blueprint(graphql_bp, url_prefix='/api/graphql')

    @app.route('/')
    def index():
        return "Testing: a (painful) checkpoint"

    if config in ['testing', 'development']:
        from app.tests_site import bp as tests_site_bp
        app.register_blueprint(tests_site_bp, url_prefix='/testing')

    return app
