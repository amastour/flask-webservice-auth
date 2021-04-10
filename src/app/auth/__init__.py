from flask import Blueprint
from flask_restplus import Api

auth_blueprint = Blueprint('auth_blueprint', __name__)
auth_api = Api(auth_blueprint,
             title='Auth API',
             version='1.0',
             description='simple api for learn')

from .views.auth import auth_ns
from .views.user import user_ns
auth_api.add_namespace(auth_ns)
auth_api.add_namespace(user_ns)