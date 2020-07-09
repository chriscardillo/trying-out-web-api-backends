from . import bp
from app import auth_manager
from flask import jsonify, request, g, session

@bp.route('/token', methods = ['GET'])
@auth_manager.login_required
def return_token():
    token = g.user.generate_auth_token()
    # is it okay to put the auth token in the session object?
    return jsonify({ 'token': token.decode('ascii') })

@bp.route('/secure', methods = ['GET'])
@auth_manager.login_required
def hello_secure():
    return jsonify({'message': 'hello ' + g.user.username + '! The secret message is ' + session['test']})
