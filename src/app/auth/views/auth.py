from flask import request
from flask_restplus import Resource, Namespace
from app.auth import auth_api
from ..models.user import User as UserModel
from ..controllers.auth import  login_user, logout_user
import logging
log = logging.getLogger(__name__)

auth_ns = Namespace('auth', description="authentication related operations")

@auth_ns.route("/login")
class UserLogin(Resource):

    @auth_ns.doc("user login")
    @auth_ns.expect(UserModel.auth, validate=True)
    def post(self):
        return login_user(request)


@auth_ns.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @auth_ns.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        log.debug(auth_header)
        return logout_user(data=request)