from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import auto_field,SQLAlchemySchema,SQLAlchemyAutoSchema
from marshmallow import fields,validates_schema,ValidationError

from models.database import db
from models.customer.customer_address import CustomerAddress,District,State
from schemas.schema import schema
from schemas.user.seller import SellerReadSchema

class CustomerAddressCreateSchema(schema.SQLAlchemyAutoSchema):
    building=fields.String(required=True)
    street=fields.String(required=True)
    area=fields.String(required=True)
    district_id = auto_field()
    state_id = auto_field()
    customer_id = auto_field()
    
    class Meta:
        model=CustomerAddress
        load_instance = True

class CustomerAddressReadSchema(schema.SQLAlchemySchema):
    id=fields.Integer(required=True)
    building=fields.String(required=True)
    street=fields.String(required=False)
    area=fields.String(required=True)
    district_id = auto_field()
    state_id = auto_field()
    
    class Meta:
        model=CustomerAddress
        load_instance = True
        sqla_session = db.session
        include_fk = True

class DistrictCreateSchema(schema.SQLAlchemySchema):
    name=fields.String(required=True)
    state_id=auto_field()
    
    class Meta:
        model=District
        load_instance = True
        sqla_session = db.session
        include_fk = True

class DistrictReadSchema(schema.SQLAlchemySchema):
    id=fields.Integer(required=True)
    name=fields.String(required=True)
    state_id=auto_field()
    
    class Meta:
        model=District
        load_instance = True
        sqla_session = db.session
        include_fk = True


class StateCreateSchema(schema.SQLAlchemySchema):
    name=fields.String(required=True)
    
    class Meta:
        model=State
        load_instance = True
        sqla_session = db.session
        include_fk = True


class StateReadSchema(schema.SQLAlchemySchema):
    id=fields.Integer(required=True)
    name=fields.String(required=True)
    
    class Meta:
        model=State
        load_instance = True
        sqla_session = db.session
        include_fk = True