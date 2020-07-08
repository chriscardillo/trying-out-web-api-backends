from app.models import *
from app import api_manager

api_manager.create_api(User,
                       methods=['POST', 'GET', 'PUT', 'DELETE'],
                       include_columns = ['id', 'created_at', 'username', 'email'],
                       url_prefix='/api/restless')
api_manager.create_api(Todo,
                       methods=['POST', 'GET', 'PUT', 'DELETE'],
                       include_columns=['id', 'user_id', 'created_at', 'last_updated_at', 'title'],
                       url_prefix='/api/restless')
api_manager.create_api(Manufacturer,
                       methods=['GET'],
                       url_prefix='/api/restless')
