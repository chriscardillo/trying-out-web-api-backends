import graphene
from app import db
from app.models import *
from graphql import GraphQLError
from app.auth import auth_manager
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
                token=user.generate_auth_token()
            )
        except IntegrityError:
            raise GraphQLError("Username or email already exists.")
        except AssertionError as a:
            raise GraphQLError(a)
        except:
            raise GraphQLError("Please check your request and try again.")

class Login(graphene.Mutation):
    """Use your username and password to receive a token."""
    token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, password):
        user = User.query.filter(User._username == User.searchable(username)).first()
        if user and user.check_password(password):
            token = user.generate_auth_token()
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
            token = user.generate_auth_token()
            return UpdatePassword(
                token=token
            )
        except:
            raise GraphQLError("Unknown Error.")

class AuthMutations:
    register=Register.Field()
    login=Login.Field()
    update_password=UpdatePassword.Field()
