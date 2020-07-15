from app.models import User
from sqlalchemy import func
from flask_httpauth import HTTPBasicAuth

auth_manager = HTTPBasicAuth()

@auth_manager.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if user:
        verified = user
    else:
        user = User.query.filter(func.lower(User.username) == username_or_token.lower().replace(" ", "")).first()
        if user and user.check_password(password):
            verified = user
        else:
            verified = False
    return verified

@auth_manager.error_handler
def auth_error(status):
    return "Please pass a valid username:password or a valid token:anytext using basic access authentication", status
    # if you can think of more error messages, you can pass them in via g, e.g. g.auth_manager_error_message
