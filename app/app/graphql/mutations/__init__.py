import graphene
from .auth import AuthMutations
from .user import UserMutations
from .todo import TodoMutations

class Mutations(graphene.ObjectType,
                AuthMutations,
                UserMutations,
                TodoMutations):
    pass
