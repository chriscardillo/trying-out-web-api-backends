from flask import Blueprint, g, session
from app.models import User
from app import auth_manager

bp = Blueprint('auth', __name__)

@auth_manager.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if user:
        verified = True
        g.user = user
        session['test'] = 'carrots'
        # is it okay to put the auth token in the session object?
        # then check the session for the token before we check what the user sent?
    else:
        user = User.query.filter_by(username = username_or_token.lower().replace(" ", "")).first()
        if user and user.check_password(password):
            verified = True
            g.user = user
        else:
            verified = False
    return verified

from app.auth import routes
