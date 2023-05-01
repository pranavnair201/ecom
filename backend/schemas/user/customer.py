from schemas.schema import schema
from marshmallow import fields
from marshmallow import fields,validates_schema,ValidationError
from flask import request

from models.database import db
from models.user.customer import CustomerProfile
from models.user.seller import SellerProfile

class CustomerCreateSchema(schema.SQLAlchemySchema):
    uid=fields.String(required=True)
    name=fields.String(required=True)
    email = fields.Email(required=False)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model=CustomerProfile
        load_instance=True
    
    # @validates_schema
    # def validate_user_exist(self, data, **kwargs):
    #     email=data.get('email',None)
    #     password=data.get('password',None)
    #     password=data.get('password',None)
    #     if email!=None:
    #         if request.app=='customer':
    #             user_exists=CustomerProfile.query.filter_by(email=email).count()
    #         else:
    #             user_exists=SellerProfile.query.filter_by(email=email).count()
    #     if user_exists>0:
    #         raise ValidationError(f"{request.app} does exists..!!",'exist')
        
class CustomerReadSchema(schema.SQLAlchemyAutoSchema):
    name=fields.String(required=True)
    address=fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model = CustomerProfile
        load_instance = True
        sqla_session = db.session
        include_fk = True