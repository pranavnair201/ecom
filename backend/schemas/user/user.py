import enum
from flask import request
from marshmallow import fields,validates_schema,ValidationError

from schemas.schema import schema
from models.user.customer import CustomerProfile
from models.user.seller import SellerProfile

class LoginEnum(enum.Enum):
    EMAIL=1
    PHONE=2

class LoginSchema(schema.SQLAlchemySchema):
    email = fields.Email(required=False)
    password = fields.String(required=False)
    phone_number = fields.String(required=False)
    type = fields.Integer(required=False)
    
    
    @validates_schema
    def validate_body(self, data, **kwargs):
        type=data.get('type',None)
        email=data.get('email',None)
        password=data.get('password',None)
        phone_number=data.get('phone_number',None)
        if not(bool(email) and bool(password)) and type==LoginEnum.EMAIL.value:
            raise ValidationError(f"Email/password required",'input')
        if not(bool(phone_number)) and type==LoginEnum.PHONE.value:
            raise ValidationError(f"Phone number is required",'input')

    @validates_schema
    def validate_user_exist(self, data, **kwargs):
        type=data.get('type',None)
        if type==LoginEnum.EMAIL.value:
            if request.app=='customer':
                user_exists=CustomerProfile.query.filter_by(email=data['email']).count()
            else:
                user_exists=SellerProfile.query.filter_by(email=data['email']).count()
        else:
            
            if request.app=='customer':
                user_exists=CustomerProfile.query.filter_by(phone_number=data['phone_number']).count()
            else:
                user_exists=SellerProfile.query.filter_by(phone_number=data['phone_number']).count()
        if user_exists==0:
            raise ValidationError(f"{request.app} does not exists..!!",'exist')
        
    @validates_schema
    def validate_user_password_check(self, data, **kwargs):
        type=data.get('type',None)
        if type==LoginEnum.EMAIL.value:
            if request.app=='customer':
                user_exists=CustomerProfile.query.filter_by(email=data['email'])
            else:
                user_exists=SellerProfile.query.filter_by(email=data['email'])
            user=user_exists.first()
            if user!=None:
                if user.password!=data['password']:
                    raise ValidationError("Invalid password..!!",'password')
    
    @validates_schema
    def validate_user_is_verified(self, data, **kwargs):
        type=data.get('type',None)
        if type==LoginEnum.EMAIL.value:
            if request.app=='customer':
                user_exists=CustomerProfile.query.filter_by(email=data['email'])
            else:
                user_exists=SellerProfile.query.filter_by(email=data['email'])
            user=user_exists.first()
            if user!=None:
                if not(user.is_verified):
                    raise ValidationError("Please get your email verified..!!",'verify')