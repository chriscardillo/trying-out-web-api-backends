import graphene
from app import db
from sqlalchemy import and_
from app.models import Todo, Tag
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

class UpdateTodo(graphene.Mutation):
    """Create a new Todo"""
    id = graphene.Int()
    title = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String(required=True)

    @auth_manager.login_required
    def mutate(self, info, id, **kwargs):
        user = auth_manager.current_user()
        todo = Todo.query.filter(and_(Todo.id == id, Todo.user_id == user.id)).first()
        if todo:
            try:
                todo.update(kwargs)
                db.session.commit()
                return UpdateTodo(
                    id=todo.id,
                    title=todo.title
                )
            except:
                GraphQLError("An unexpected error has occurred.")
        else:
            raise GraphQLError("Todo not owned by current user.")

class DeleteTodo(graphene.Mutation):
    """Delete a user from the database."""
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)

    @auth_manager.login_required
    def mutate(self, info, id):
        user = auth_manager.current_user()
        todo = Todo.query.filter(and_(Todo.id == id, Todo.user_id == user.id)).first()
        if todo:
            try:
                db.session.delete(todo)
                db.session.commit()
                return DeleteTodo(
                    ok = True
                )
            except:
                GraphQLError("An unexpected error has occurred.")
        else:
            raise GraphQLError("Todo not owned by current user.")

class TagTodo(graphene.Mutation):
    """Tag a Todo"""
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int(required=True)
        tag = graphene.String(required=True)

    @auth_manager.login_required
    def mutate(self, info, id, tag):
        user = auth_manager.current_user()
        todo = Todo.query.filter(and_(Todo.id == id, Todo.user_id == user.id)).first()
        existing_tag = Tag.query.filter(and_(Tag.todo_id == todo.id, Tag._tag == Tag.searchable(tag))).first()
        if existing_tag:
            raise GraphQLError("Tag already exists on todo.")
        if todo:
            try:
                new_tag = Tag(todo_id=todo.id, tag=tag)
                todo.tags.append(new_tag)
                db.session.commit()
                return TagTodo(
                    ok = True
                )
            except:
                GraphQLError("An unexpected error has occurred.")
        else:
            raise GraphQLError("Todo not owned by current user.")

class TodoMutations:
    create_todo=CreateTodo.Field()
    update_todo=UpdateTodo.Field()
    delete_todo=DeleteTodo.Field()
    tag_todo=TagTodo.Field()
