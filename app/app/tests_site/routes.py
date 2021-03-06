from . import bp
from app.auth import auth_manager
from flask import jsonify, session

@bp.route('/')
def site():
    return "This is where the site lives!"

@bp.route('/secure', methods = ['GET'])
@auth_manager.login_required
def hello_secure():
    current_user = auth_manager.current_user()
    secret_message = "nothing!"
    return jsonify({'message': 'hello ' + current_user.username + '! The secret message is ' + secret_message})
