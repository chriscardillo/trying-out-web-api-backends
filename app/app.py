import os
import flask
import flask_sqlalchemy
import flask_restless
from flask_migrate import Migrate

# App
app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')


# DB
db = flask_sqlalchemy.SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True, nullable=False)
    email = db.Column(db.Unicode, unique=True, nullable=False)

# Routes
@app.route('/', methods=['GET'])
def home():
    return """
           <h1>Back at it again</h1>
           <p>Can't leave flask alone</p>
           <p>(restless edition)</p>
           """

# API
manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Users, methods=['POST', 'GET', 'PUT', 'DELETE'])

# RUN
if __name__ == '__main__':
    app.run(host='0.0.0.0')
