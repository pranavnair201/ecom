import os
from flask import request,make_response
from flask_restful import Resource
from flasgger import swag_from

from services.user_service import UserService
from schemas.user.customer import CustomerCreateSchema
from schemas.user.seller import SellerCreateSchema
from schemas.user.user import LoginSchema
from models.database import db
from utils.jwt import validate_token
from utils.error_handler import error_handler
from swagger.swagger import route

class UserCreateView(Resource):
    user_service=UserService()
    db_session=db.session
    
    @swag_from(os.path.join(route,'user/signup_customer.yml'))
    @error_handler
    def post(self):
        data = request.get_json()
        if request.app=='customer':
            error=CustomerCreateSchema().validate(data,session=self.db_session)
            if error:
                return make_response({"status":False, "detail":error},400)
            user=CustomerCreateSchema().load(data,session=db.session)
        else:
            error=SellerCreateSchema().validate(data,session=self.db_session)
            if error:
                return make_response({"status":False, "detail":error},400)
            user=SellerCreateSchema().load(data,session=db.session)
        return self.user_service.sign_up(user)
    
    @validate_token
    @error_handler
    def get(self):
        return self.user_service.get_profile()

class UserLoginView(Resource):
    user_service=UserService()
    db_session=db.session
    
    @swag_from(os.path.join(route,'user/login.yml'))
    @error_handler
    def post(self):
        data = request.get_json()
        error=LoginSchema().validate(data)
        if error:
            return make_response({"status":False, "detail":error},400)
        return self.user_service.login(data)

class UserVerifyView(Resource):
    user_service=UserService()
    db_session=db.session
    
    def get(self):
        args=request.args.to_dict()
        token=args['token']
        if token==None:
            return make_response({"status":False, "detail":"Token not provided"},400)
        app=args['app']
        if app==None:
            return make_response({"status":False, "detail":"App not provided"},400)
        return self.user_service.verify_user(token,app)