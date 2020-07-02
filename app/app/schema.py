import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .objects import *
from .models import *

class Query(graphene.ObjectType):

    user_todos = graphene.List(TodoObject, username=graphene.String())

    @staticmethod
    def resolve_user_todos(self, info, **args):
        username = args.get('username')
        todo_query = TodoObject.get_query(info)
        return todo_query.join(User).filter(User.username == username).all()

schema = graphene.Schema(query=Query)
