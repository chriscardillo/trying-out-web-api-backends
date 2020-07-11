import graphene
from app import db
import sys
from app.models import *
from app.auth import auth_manager
from graphql import GraphQLError
from sqlalchemy.exc import IntegrityError

class Login(graphene.Mutation):
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

class Register(graphene.Mutation):
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

class UpdateUser(graphene.Mutation):
    token = graphene.String()

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    @auth_manager.login_required
    def mutate(self, info, **kwargs):
        # should this be a decorator?
        try:
            user = auth_manager.current_user()
            user.update(kwargs)
            db.session.commit()
            return UpdateUser(
                token=user.generate_auth_token().decode('ascii')
            )
        except IntegrityError:
            raise GraphQLError("Username or email already exists.")
        except:
            raise GraphQLError("Please check your request and try again.")

class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        ok = graphene.Boolean()

    @auth_manager.login_required
    def mutate(self, info):
        user = auth_manager.current_user()
        db.session.delete(user)
        db.session.commit()
        return DeleteUser(ok = True)
