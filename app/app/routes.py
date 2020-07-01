from app import app, db
from .models import User
from .schema import schema
from flask_graphql import GraphQLView
import flask_restless

@app.route('/')
@app.route('/index')
def index():
    return "Hello, Flask!"

app.add_url_rule('/api/graphql',
                 view_func=GraphQLView.as_view(
                     'graphql',
                     schema=schema,
                     graphiql=True
                 )
)

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(User,
                   methods=['POST', 'GET', 'PUT', 'DELETE'],
                   url_prefix='/api/restless')
