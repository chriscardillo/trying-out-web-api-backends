from .schema import schema
from flask_graphql import GraphQLView

from . import bp

bp.add_url_rule('/',
                 view_func=GraphQLView.as_view(
                     'graphql',
                     schema=schema,
                     graphiql=True
                 )
)
