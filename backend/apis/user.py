import os
import uuid
from flask import request,make_response
from flask_restful import Resource
from flasgger import swag_from

# from firebase_token_generator import create_token
# from utils.firebase.firebase import FirebaseHandler
from services.user_service import UserService
from schemas.user.customer import CustomerCreateSchema
from schemas.user.seller import SellerCreateSchema
from schemas.user.user import LoginSchema
from models.database import db
from utils.jwt import validate_token
from utils.error_handler import error_handler
from swagger.swagger import route
from utils.twilio import phone_auth

class UserCreateView(Resource):
    user_service=UserService()
    db_session=db.session
    # auth_handler=FirebaseHandler()
    
    @swag_from(os.path.join(route,'user/signup_customer.yml'))
    @error_handler
    def post(self):
        # request.app='customer'
        data = request.get_json()
        
        # data['uid']=self.auth_handler.create_uid(data)
        data['uid']=str(uuid.uuid4())
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
        print(user.uid)
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
    
    # @error_handler
    def post(self):
        request.app='seller'
        data=request.get_json()
        return self.user_service.verify_otp(data)