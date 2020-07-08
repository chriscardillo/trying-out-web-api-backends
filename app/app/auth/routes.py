from . import bp
import subprocess
from app.models import User
from app import auth_manager
from flask import jsonify, request, g
from flask_restless import ProcessingException

@auth_manager.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if user:
        verified = True
        g.user = user
    else:
        user = User.query.filter_by(username = username_or_token.lower().replace(" ", "")).first()
        if user and user.check_password(password):
            verified = True
            g.user = user
        else:
            verified = False
    return verified

@bp.route('/token', methods = ['GET'])
@auth_manager.login_required
def return_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })


@bp.route('/secure', methods = ['GET'])
@auth_manager.login_required
def hello_secure():
    return jsonify({'message': 'hello from a secure world, ' + g.user.username + '!'})
