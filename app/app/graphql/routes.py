from .schema import schema
from flask_graphql import GraphQLView
from app import auth_manager

from . import bp

def graphql_view():
    view = GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
    return auth_manager.login_required(view)

bp.add_url_rule('/',
                view_func=graphql_view()
)
