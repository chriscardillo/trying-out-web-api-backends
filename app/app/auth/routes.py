from . import bp
from app.models import User
from app import auth_manager
from flask import jsonify, request
from flask_restless import ProcessingException

@auth_manager.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username = username.lower().replace(" ", "")).first()
    if not user or not user.check_password(password):
        verified = False
    else:
        verified = True
        #g.user = user
    return verified

@bp.route('/test', methods = ['GET'])
@auth_manager.login_required
def test():
    return jsonify({"you": "did it"})

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
