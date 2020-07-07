from flask import Blueprint

bp = Blueprint('restless', __name__)

from app.restless import routes
