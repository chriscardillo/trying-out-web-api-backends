import graphene
from app import db
import sys
from app.models import *
from app.auth import auth_manager
from graphql import GraphQLError
from sqlalchemy.exc import IntegrityError

class CreateUser(graphene.Mutation):
    token = graphene.String()

    class Arguments:
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, **kwargs):
        # should this be a decorator?
        try:
            user=User(**kwargs)
            db.session.add(user)
            db.session.commit()
            return CreateUser(
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
            for k, v in kwargs.items():
                setattr(user, k, v)
            db.session.commit()
            return UpdateUser(
                token=user.generate_auth_token().decode('ascii')
            )
        except IntegrityError:
            raise GraphQLError("Username or email already exists.")
        except:
            raise GraphQLError("Please check your request and try again.")
