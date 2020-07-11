import graphene
from app.graphql.queries import Queries
from app.graphql.mutations import Mutations

schema = graphene.Schema(query=Queries, mutation=Mutations)
