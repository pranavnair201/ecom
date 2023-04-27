from flask import request
from marshmallow import fields,validates_schema,ValidationError


from schemas.schema import schema
from models.user.customer import Customer
from models.user.seller import Seller

class LoginSchema(schema.SQLAlchemySchema):
    email = fields.Email(required=True)
    password = fields.String(required=True)
    
    @validates_schema
    def validate_user_exist(self, data, **kwargs):
        if request.app=='customer':
            user_exists=Customer.query.filter_by(email=data['email']).count()
        else:
            user_exists=Seller.query.filter_by(email=data['email']).count()
        if user_exists==0:
            raise ValidationError(f"{request.app} does not exists..!!",'exist')
        
    @validates_schema
    def validate_user_password_check(self, data, **kwargs):
        if request.app=='customer':
            user_exists=Customer.query.filter_by(email=data['email'])
        else:
            user_exists=Seller.query.filter_by(email=data['email'])
        user=user_exists.first()
        if user!=None:
            if user.password!=data['password']:
                raise ValidationError("Invalid password..!!",'password')
    
    @validates_schema
    def validate_user_is_verified(self, data, **kwargs):
        if request.app=='customer':
            user_exists=Customer.query.filter_by(email=data['email'])
        else:
            user_exists=Seller.query.filter_by(email=data['email'])
        user=user_exists.first()
        if user!=None:
            if not(user.is_verified):
                raise ValidationError("Please get your email verified..!!",'verify')