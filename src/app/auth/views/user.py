from flask_restplus import Resource, Namespace
from app.auth import auth_api
from ..models.user import User as UserModel
from ..controllers.user import  get_user, create_user
from ..utils.decorator import token_required
import logging
log = logging.getLogger(__name__)
from config import key
user_ns = Namespace("user", "User operations")


@user_ns.route("/")
class UserList(Resource):
    @user_ns.doc('list_of_registered_users')
    @token_required
    @user_ns.marshal_list_with(UserModel.user, envelope='data')
    def get(self):
        """List all registered users"""
        #log.debug(key)
        return get_user()

    @user_ns.response(201, 'User successfully created.')
    @user_ns.doc('create a new user')
    @user_ns.expect(UserModel.user, validate=True)
    def post(self):
        """Creates a new User """
        return create_user(auth_api.payload)

@user_ns.route('/<public_id>')
@user_ns.param('public_id', 'The User identifier')
@user_ns.response(404, 'User not found.')
class User(Resource):
    @user_ns.doc('get a user')
    @user_ns.marshal_with(UserModel.user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user