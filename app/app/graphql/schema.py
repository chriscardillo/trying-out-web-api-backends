import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .objects import *
from .mutations import *
from app.models import *
from app import auth_manager

class Query(graphene.ObjectType):

    user = graphene.Field(UserObject, username=graphene.String())

    #@auth_manager.login_required
    def resolve_user(self, info, username):
        query = UserObject.get_query(info)
        query = query.filter(User.username == username.lower().replace(" ", ""))
        return query.first()

class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
