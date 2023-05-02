import os
from flask import make_response,request
from flask_mail import Message
from schemas.user.user import LoginEnum
import logging

from utils.twilio import phone_auth,service
from models.database import db
from models.user.customer import CustomerProfile
from models.user.seller import SellerProfile
from utils.jwt import generate_token,verify_user_token
from utils.mail_handler import mail

class UserService():
    
    def sign_up(self,user):
        if user.email!=None:
            msg = Message(
                'Verify your email id',
                sender =os.environ.get('EMAIL_ID'),
                recipients = [user.email]
            )
            token=str(generate_token(LoginEnum.EMAIL.value,user.email))
            link=os.environ.get('VERIFICATION_LINK')+f"?token={token}&app={request.app}"
            msg.body = f'verification link - {link}'
            mail.send(msg)
        db.session.add(user)
        db.session.commit()
        return make_response({"status":True, "detail":"User created successfully"},200)
    
    def verify_user(self,token,app):
        email=verify_user_token(token)
        if app=='customer':
            user=CustomerProfile.query.filter_by(email=email).one_or_none()
        else:
            user=SellerProfile.query.filter_by(email=email).one_or_none()
        if user==None:
            return make_response({"status":False, "detail":"User does not exist"},404)
        user.is_verified=True
        db.session.commit()
        return make_response({"status":True, "detail":"User verified successfully"},200)
    
    def login(self,data):
        type=data.get('type',None)
        if type==LoginEnum.PHONE.value:
            phone_number=data.get('phone_number',None)
            print(phone_number)
            check=phone_auth.verify \
                     .v2 \
                     .services(service.sid) \
                     .verifications \
                     .create(to='+91'+str(phone_number), channel='sms')
            return make_response({"status":True,"detail":"OTP sent to mobile"},200)
        
        if request.app=='customer':
            user_exists=CustomerProfile.query.filter_by(email=data['email'])
        else:
            user_exists=SellerProfile.query.filter_by(email=data['email'])
        user=user_exists.first()
        token=generate_token(LoginEnum.EMAIL.value, user.email)
        return make_response({"token":token,"id":user.uid},200)
    
    def verify_otp(self,data):
        otp=data.get('otp',None)
        phone_number=data.get('phone_number',None)
        verification_check = phone_auth.verify \
                           .v2 \
                           .services(service.sid) \
                           .verification_checks \
                           .create(to='+91'+str(phone_number), code=otp)
        if verification_check.status=='approved':
            print(CustomerProfile.query.all()[0].phone_number)
            if request.app=='customer':
                user_exists=CustomerProfile.query.filter_by(phone_number=data['phone_number'])
            else:
                user_exists=SellerProfile.query.filter_by(phone_number=data['phone_number'])
            user=user_exists.first()
            if user!=None:
                token=generate_token(LoginEnum.PHONE.value,user.phone_number)
                return make_response({"status":True,"token":token,"detail":"Verified"},200)
            return make_response({"status":False,"detail":"User does not exist"},200)
        return make_response({"status":False,"detail":"Wrong OTP"},400)