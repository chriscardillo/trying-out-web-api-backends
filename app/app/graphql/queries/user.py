import graphene
from .todo import TodoObject
from app.models import User, Todo
from graphene_sqlalchemy import SQLAlchemyObjectType

class UserObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = User
        only_fields=('id', 'email', 'todos')
        #interfaces = (graphene.relay.Node,)

    todos = graphene.List(lambda: TodoObject, last=graphene.Int())
    def resolve_todos(self, info, last=None):
        max=10
        if last and last < max:
            max = last
        todo_query = TodoObject.get_query(info).filter(Todo.user_id == self.id)
        return todo_query.order_by(Todo.updated_at.desc()).limit(max).all()

class UserQuery:
    user = graphene.Field(UserObject, username=graphene.String(required=True))

    def resolve_user(self, info, username):
        query = UserObject.get_query(info)
        query = query.filter(User.username == username.lower().replace(" ", ""))
        return query.first()
