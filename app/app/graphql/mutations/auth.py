import graphene
from app import db
from app.models import *
from app.auth import auth_manager
from graphql import GraphQLError
from sqlalchemy.exc import IntegrityError

class Register(graphene.Mutation):
    """Register for the service and receive a token."""
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, **kwargs):
        # should this be a decorator?
        try:
            user=User(**kwargs)
            db.session.add(user)
            db.session.commit()
            return Register(
                token=user.generate_auth_token().decode('ascii')
            )
        except IntegrityError:
            raise GraphQLError("Username or email already exists.")
        except:
            raise GraphQLError("Please check your request and try again.")

class Login(graphene.Mutation):
    """Use your username and password to receive a token."""
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = User.query.filter_by(username = username.lower().replace(" ", "")).first()
        if user and user.check_password(password):
            token = user.generate_auth_token().decode('ascii')
        else:
            raise GraphQLError("Incorrect username or password.")
        return Login(
            token=token
        )

class UpdatePassword(graphene.Mutation):
    """Update password and receive a new token."""
    token = graphene.String()

    class Arguments:
        password = graphene.String(required=True)

    @auth_manager.login_required
    def mutate(self, info, password):
        try:
            user = auth_manager.current_user()
            user.update(dict(password=password))
            db.session.commit()
            token = user.generate_auth_token().decode('ascii')
        except:
            raise GraphQLError("Unknown Error.")
        return UpdatePassword(
            token=token
        )

class AuthMutations:
    register=Register.Field()
    login=Login.Field()
    update_password=UpdatePassword.Field()
