from flask import Blueprint

bp = Blueprint('site', __name__)

from app.tests_site import routes
