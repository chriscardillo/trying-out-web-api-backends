import graphene
from .auth import AuthMutations
from .user import UserMutations

class Mutations(graphene.ObjectType,
                AuthMutations,
                UserMutations):
    pass
