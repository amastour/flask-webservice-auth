from ..models.user import User as UserModel
from app import db
import uuid
import datetime
import logging
log = logging.getLogger(__name__)

def save_changes(data):
    db.session.add(data)
    db.session.commit()

def get_user(public_id=None):
    if public_id is None:
        return UserModel.query.all()
    else:
        return UserModel.query.filter_by(public_id= public_id).first_or_404()

def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401

def create_user(data):
    user = UserModel.query.filter_by(email=data['email']).first()
    if not user:
        new_user = UserModel(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409
