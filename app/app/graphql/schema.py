import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .objects import *
from app.graphql.mutations import Mutations
from app.models import *

class Query(graphene.ObjectType):

    user = graphene.Field(UserObject, username=graphene.String(required=True))

    def resolve_user(self, info, username):
        query = UserObject.get_query(info)
        query = query.filter(User.username == username.lower().replace(" ", ""))
        return query.first()

schema = graphene.Schema(query=Query, mutation=Mutations)
