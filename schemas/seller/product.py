from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import auto_field,SQLAlchemySchema,SQLAlchemyAutoSchema
from marshmallow import fields,validates_schema,ValidationError

from models.database import db
from models.seller.product import Product
from schemas.schema import schema
from schemas.user.seller import SellerReadSchema

class ProductCreateSchema(schema.SQLAlchemyAutoSchema):
    name=fields.String(required=True)
    price=fields.Integer(required=True)
    quantity=fields.Integer(required=True)
    seller_id = auto_field()
    
    class Meta:
        model=Product
        load_instance = True

class ProductReadSchema(schema.SQLAlchemySchema):
    id=fields.Integer(required=True)
    name=fields.String(required=True)
    price=fields.Integer(required=True)
    quantity=fields.Integer(required=True)
    seller = fields.Nested(SellerReadSchema,many=False,exclude=['password'])
    
    class Meta:
        model=Product
        load_instance = True
        sqla_session = db.session
        include_fk = True