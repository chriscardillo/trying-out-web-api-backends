import graphene
from app import db
from app.models import Todo
from app.auth import auth_manager
from graphql import GraphQLError
from sqlalchemy.exc import IntegrityError

class CreateTodo(graphene.Mutation):
    """Create a new Todo"""
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        title = graphene.String()

    @auth_manager.login_required
    def mutate(self, info, title):
        try:
            user = auth_manager.current_user()
            todo = Todo(user_id = user.id,
                        title = title)
            db.session.add(todo)
            db.session.commit()
            return CreateTodo(
                id=todo.id,
                title=todo.title
            )
        except:
            raise GraphQLError("You are probably not authorized to be here.")

class TodoMutations:
    create_todo=CreateTodo.Field()
