import graphene
from app.models import Todo
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene_sqlalchemy import SQLAlchemyConnectionField

class TodoObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = Todo
        exclude_fields=('user', 'user_id')
