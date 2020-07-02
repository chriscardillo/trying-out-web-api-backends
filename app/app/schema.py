import graphene
from graphene_sqlalchemy import SQLAlchemyConnectionField
from .objects import *
from .models import *

class Query(graphene.ObjectType):

    user_todos = graphene.List(TodoObject, username=graphene.String(), last=graphene.Int())

    # Pagination would be good
    # As would some sort of search on the title level?
    @staticmethod
    def resolve_user_todos(self, info, **args):
        username = args.get('username')
        last = args.get('last')
        max = 10
        todo_query = TodoObject.get_query(info)
        todo_query = todo_query.join(User).filter(User.username == username)
        if last and last < max:
            max = last
        return todo_query.order_by(Todo.last_updated_at.desc()).limit(max).all()

schema = graphene.Schema(query=Query)
