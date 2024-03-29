import os
import jwt
import datetime
from flask import make_response, request

from schemas.user.user import LoginEnum
from models.user.customer import CustomerProfile
from models.user.seller import SellerProfile

def generate_token(type,identity):
    payload={
        "type":type,
        "identity":identity,
        "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=45)
    }
    secret = os.environ.get('TOKEN_SECRET')
    token=jwt.encode(payload,secret)
    return token


def verify_user_token(token):
    secret = os.environ.get('TOKEN_SECRET')
    try:
        data=jwt.decode(token, secret, algorithms=["HS256"])
    except jwt.exceptions.ExpiredSignatureError:
        return make_response({"status":False,"detail": "Token Expired"}, 400)
    except jwt.exceptions.DecodeError:
        return make_response({"status":False,"detail": "Token Invalid"}, 400)
    except Exception as e:
        return make_response({"status":False,"message": "Invalid token provided"}, 403)
    if data['type']!=LoginEnum.EMAIL.value:
        return make_response({"status":False,"message": "Its only for email verification"}, 400)
    return data['identity']

def validate_token(func):
    secret = os.environ.get('TOKEN_SECRET')
    
    def wrapper(*args, **kwargs):
        try:
            token = request.headers['token']
        except Exception as e:
            return make_response({"message": "Token not provided"}, 403)
        
        try:
            data=jwt.decode(token, secret, algorithms=["HS256"])
        except jwt.exceptions.ExpiredSignatureError:
            return make_response({"status":False,"detail": "Token Expired"}, 400)
        except jwt.exceptions.DecodeError:
            return make_response({"status":False,"detail": "Token Invalid"}, 400)
        except Exception as e:
            return make_response({"status":False,"message": "Invalid token provided"}, 403)
        
        try:
            app = request.headers['app']
        except Exception as e:
            return make_response({"message": "App not provided"}, 403)
        if app not in ['seller','customer']:
            return make_response({"message": "App is invalid"}, 403)
        request.app=app
        if data['type']==LoginEnum.PHONE.value:
            if request.app=='seller':
                request.user=SellerProfile.query.filter_by(phone_number=data['identity']).one_or_none()
            else:
                request.user=CustomerProfile.query.filter_by(phone_number=data['identity']).one_or_none()
        else:
            if request.app=='seller':
                request.user=SellerProfile.query.filter_by(email=data['identity']).one_or_none()
            else:
                request.user=CustomerProfile.query.filter_by(email=data['identity']).one_or_none()
        if request.user==None:
            return make_response({"status":False,"message": "Unauthorized user"}, 403)
        return func(*args, **kwargs)
    return wrapper