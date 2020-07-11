import graphene
from app import db
from app.models import *
from app.auth import auth_manager
from graphql import GraphQLError
from sqlalchemy.exc import IntegrityError

class UpdateUser(graphene.Mutation):
    """Update a user's information, like their username or email."""
    ok = graphene.Boolean()

    class Arguments:
        username = graphene.String()
        email = graphene.String()

    @auth_manager.login_required
    def mutate(self, info, **kwargs):
        # should this be a decorator?
        try:
            user = auth_manager.current_user()
            user.update(kwargs)
            db.session.commit()
            return UpdateUser(
                ok = True
            )
        except IntegrityError:
            raise GraphQLError("Username or email already exists.")
        except:
            raise GraphQLError("Please check your request and try again.")

class DeleteUser(graphene.Mutation):
    """Delete a user from the database."""
    ok = graphene.Boolean()

    class Arguments:
        ok = graphene.Boolean()

    @auth_manager.login_required
    def mutate(self, info):
        user = auth_manager.current_user()
        db.session.delete(user)
        db.session.commit()
        return DeleteUser(
            ok=True
        )

class UserMutations:
    update_user=UpdateUser.Field()
    delete_user=DeleteUser.Field()
