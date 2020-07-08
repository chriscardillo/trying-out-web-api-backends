from . import bp
from app import auth_manager
from flask import jsonify, request, g

@bp.route('/token', methods = ['GET'])
@auth_manager.login_required
def return_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

@bp.route('/secure', methods = ['GET'])
@auth_manager.login_required
def hello_secure():
    return jsonify({'message': 'hello from a secure world, ' + g.user.username + '!'})
