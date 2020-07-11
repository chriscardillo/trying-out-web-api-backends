import graphene
from .auth import Register, Login, UpdatePassword
from .user import UpdateUser, DeleteUser

class Mutations(graphene.ObjectType):
    # auth mutations
    register=Register.Field()
    login=Login.Field()
    update_password=UpdatePassword.Field()

    # user mutations
    update_user=UpdateUser.Field()
    delete_user=DeleteUser.Field()
