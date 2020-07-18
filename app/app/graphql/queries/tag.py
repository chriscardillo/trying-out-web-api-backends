import graphene
from app.models import Tag
from graphene_sqlalchemy import SQLAlchemyObjectType

class TagObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = Tag
        only_fields=('id', 'tag', 'tag_standard',
                     'created_at', 'updated_at',)
