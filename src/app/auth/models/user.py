from flask_restplus import fields
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import datetime
import jwt
from app import db, flask_bcrypt
from app.auth import auth_api
from config import key
import logging
from ..models.blacklist import Blacklist as BlacklistModel


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True,nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    public_id = db.Column(db.String(20), unique=True )
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    refresh_tokens = relationship('RefreshToken', backref='user')


    @property
    def password(self):
        raise AttributeError('password:  write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode("utf-8")
    
    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return "<User '{}'>".format(self.username)
    
    def encode_auth_token(self, user_id):
        try:
            playload = {
                "exp": datetime.datetime.now() + datetime.timedelta(days=1, seconds=5),
                "iat": datetime.datetime.now(),
                "sub": user_id
            }
            return jwt.encode(
                playload,
                key,
                algorithm="HS256"
            )
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            playload = jwt.decode(auth_token, key, algorithms=["HS256"])
            is_blacklisted_token = BlacklistModel.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return playload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired, Please login again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please login again"

    user = auth_api.model("User", {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })

    auth = auth_api.model('Auth', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })




class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    refresh_token = db.Column(db.String(50), unique=True)
    user_agent_hash = db.Column(db.String(80))
