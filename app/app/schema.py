import graphene
from .objects import *

class Query(graphene.ObjectType):

    user = graphene.Field(UserObject,
                          id=graphene.Int(),
                          username=graphene.String())

    def resolve_user(self, info, **kwargs):
        query = UserObject.get_query(info)
        query = query.filter_by(**kwargs)
        return query.first()

    manufacturer = graphene.Field(ManufacturerObject,
                                  manufacturer=graphene.String())

    def resolve_manufacturer(self, info, **kwargs):
        query = ManufacturerObject.get_query(info)
        query = query.filter_by(**kwargs)
        return query.first()

schema = graphene.Schema(query=Query)
