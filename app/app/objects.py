import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import *

class UserObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = User
        only_fields=('todos')
        #interfaces

    # Pagination would be good, maybe an arg for offset
    # As would some sort of search on the title level?
    todos = graphene.List(lambda: TodoObject, last=graphene.Int())
    def resolve_todos(self, info, last=None):
        max=10
        if last and last < max:
            max = last
        # Important that users can only see information available to them
        # There has to be a better way to do this
        # (Note: the regular resolver gets to todos but doesn't paginate/offset)
        todo_query = TodoObject.get_query(info).filter(Todo.user_id == self.id)
        return todo_query.order_by(Todo.last_updated_at.desc()).limit(max).all()



class TodoObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = Todo
        exclude_fields=('user', 'user_id')

class ManufacturerObject(SQLAlchemyObjectType):

    class Meta:
        model = Manufacturer
        interfaces = (graphene.relay.Node,)
