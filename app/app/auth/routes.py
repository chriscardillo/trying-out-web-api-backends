from . import bp
from app.models import User
from flask import jsonify, request
from flask_restless import ProcessingException

# This is janky
@bp.route('/login', methods = ['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    results = {"token": None, "message": "Please provide correct username and password"}
    if username is not None and password is not None:
        user = User.query.filter_by(username = username.lower().replace(" ", "")).first()
    else:
        user=None
    if user is not None and user.check_password(password):
        results['token'] = "this_is_a_token"
        results['message'] = None
    return jsonify(results)
