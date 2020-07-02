import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import *

class UserObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = User

class TodoObject(SQLAlchemyObjectType):

    #id = graphene.Int()

    class Meta:
        model = Todo

class ManufacturerObject(SQLAlchemyObjectType):

    class Meta:
        model = Manufacturer
        interfaces = (graphene.relay.Node,)
