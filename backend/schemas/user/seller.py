from schemas.schema import schema
from marshmallow import fields,validates_schema,ValidationError
from flask import request

from models.user.customer import CustomerProfile
from models.user.seller import SellerProfile
from models.database import db

class SellerCreateSchema(schema.SQLAlchemySchema):
    uid=fields.String(required=True)
    shop_name=fields.String(required=True)
    address=fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model=SellerProfile
        load_instance=True
    
    @validates_schema
    def validate_user_exist(self, data, **kwargs):
        if request.app=='customer':
            user_exists=CustomerProfile.query.filter_by(email=data['email']).count()
        else:
            user_exists=SellerProfile.query.filter_by(email=data['email']).count()
        if user_exists>0:
            raise ValidationError(f"{request.app} does exists..!!",'exist')
        

class SellerReadSchema(schema.SQLAlchemyAutoSchema):
    shop_name=fields.String(required=True)
    address=fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model = SellerProfile
        load_instance = True
        sqla_session = db.session
        include_fk = True