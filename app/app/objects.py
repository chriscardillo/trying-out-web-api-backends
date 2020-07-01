import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import *

class UserObject(SQLAlchemyObjectType):

    id = graphene.Int()

    class Meta:
        model = User
