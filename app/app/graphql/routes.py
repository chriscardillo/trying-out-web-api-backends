from . import bp
from .schema import schema
from flask_graphql import GraphQLView

def graphql_view():
    view = GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
    return view

bp.add_url_rule('/',
                view_func=graphql_view()
)
