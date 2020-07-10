from . import bp
from app import auth_manager
from flask import jsonify, session

@bp.route('/token', methods = ['GET'])
@auth_manager.login_required
def return_token():
    token = auth_manager.current_user().generate_auth_token()
    # is it okay to put the auth token in the session object?
    return jsonify({ 'token': token.decode('ascii') })
