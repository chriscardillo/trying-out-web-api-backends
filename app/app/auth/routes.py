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

@bp.route('/token', methods = ['GET'])
@auth_manager.login_required
def return_token():
    return jsonify({"token": "your_special_token"})
