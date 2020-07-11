import graphene
from app.models import *
from .user import UserQuery

class Queries(graphene.ObjectType,
              UserQuery):
    pass
