import graphene
from .tag import TagObject
from app.models import Todo, Tag
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField

class TodoObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = Todo
        exclude_fields=('user', 'user_id')

    tags = graphene.List(lambda: TagObject)
    def resolve_tags(self, info):
        tag_query = TagObject.get_query(info).filter(Tag.todo_id == self.id)
        return tag_query.order_by(Tag.tag_standard).all()
