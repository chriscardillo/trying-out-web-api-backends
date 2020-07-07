from flask import Blueprint

bp = Blueprint('graphql', __name__)

from app.graphql import routes
