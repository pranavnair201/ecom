from schemas.schema import schema
from marshmallow import fields

from models.user.seller import Seller
from models.database import db

class SellerCreateSchema(schema.SQLAlchemySchema):
    shop_name=fields.String(required=True)
    address=fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model=Seller
        load_instance=True

class SellerReadSchema(schema.SQLAlchemyAutoSchema):
    shop_name=fields.String(required=True)
    address=fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model = Seller
        load_instance = True
        sqla_session = db.session
        include_fk = True