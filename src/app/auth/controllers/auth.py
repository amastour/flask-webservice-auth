from ..models.user import User as UserModel
from ..models.blacklist import Blacklist as BlacklistModel
from app import db
import logging
log = logging.getLogger(__name__)

def login_user(data):
    try:
        # fetch the user data
        # user_agent = new_request.user_agent.encode("utf-8")
        log.debug(data.user_agent)
        data = data.get_json()
        user = UserModel.query.filter_by(email=data.get('email')).first()
        if user and user.check_password(data.get('password')):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'Authorization': auth_token
                }
                return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'email or password does not match.'
            }
            return response_object, 401

    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again'
        }
        return response_object, 500

def get_logged_in_user(new_request):
    # get the auth token
    auth_token = new_request.headers.get('Authorization').split(" ")[1]
    log.debug(auth_token)
    
    if auth_token:
        resp = UserModel.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = UserModel.query.filter_by(id=resp).first()
            response_object = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'registered_on': str(user.registered_on)
                }
            }
            return response_object, 200
        response_object = {
            'status': 'fail',
            'message': resp
        }
        return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return response_object, 401

def logout_user(data):
    if data:
        auth_token = data.headers.get('Authorization').split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        resp = UserModel.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            return save_token(token=auth_token)
        else:
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
    else:
        response_object = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return response_object, 403

def save_token(token):
    blacklist_token = BlacklistModel(token=token)
    try:
        # insert the token
        db.session.add(blacklist_token)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully logged out.'
        }
        return response_object, 200
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': e
        }
        return response_object, 200