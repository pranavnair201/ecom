import os
from flask import make_response,request
from flask_mail import Message

from models.database import db
from models.user.customer import Customer
from models.user.seller import Seller
from utils.jwt import generate_token,verify_user_token
from utils.mail_handler import mail

class UserService():
    def sign_up(self,user):
        msg = Message(
            'Verify your email id',
            sender =os.environ.get('EMAIL_ID'),
            recipients = [user.email]
        )
        token=str(generate_token(user.email))
        link=os.environ.get('VERIFICATION_LINK')+f"?token={token}&app={request.app}"
        msg.body = f'verification link - {link}'
        mail.send(msg)
        db.session.add(user)
        db.session.commit()
        return make_response({"status":True, "detail":"User created successfully"},200)
    
    def verify_user(self,token,app):
        email=verify_user_token(token)
        if app=='customer':
            user=Customer.query.filter_by(email=email).one_or_none()
        else:
            user=Seller.query.filter_by(email=email).one_or_none()
        if user==None:
            return make_response({"status":False, "detail":"User does not exist"},404)
        user.is_verified=True
        db.session.commit()
        return make_response({"status":True, "detail":"User verified successfully"},200)
    
    def login(self,data):
        if request.app=='customer':
            user_exists=Customer.query.filter_by(email=data['email'])
        else:
            user_exists=Seller.query.filter_by(email=data['email'])
        user=user_exists.first()
        token=generate_token(user.email)
        return make_response({"token":token,"id":user.id},200)