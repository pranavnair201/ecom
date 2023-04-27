from marshmallow import fields,validates_schema,ValidationError

from models.database import db
from schemas.schema import schema
from models.orders.order import Order
from models.orders.order_item import OrderItem
from schemas.user.seller import SellerReadSchema
from schemas.customer.customer_address import CustomerAddressReadSchema
from schemas.user.customer import CustomerReadSchema
from schemas.seller.product import ProductReadSchema

class OrderSchema(schema.SQLAlchemySchema):
    payment_mode = fields.Integer(required=True)
    order_items=fields.List(fields.Dict,required=True)
    customer_id = fields.Integer()
    customer_address_id = fields.Integer()
    seller_id = fields.Integer()

class OrderItemSchema(schema.SQLAlchemySchema):
    rate = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    order_id = fields.Integer()
    product_id = fields.Integer()
    
class OrderItemReadSchema(schema.SQLAlchemySchema):
    rate = fields.Integer(required=True)
    quantity = fields.Integer(required=True)
    product = fields.Nested(ProductReadSchema,many=False)
    
    class Meta:
        model=OrderItem
        load_instance = True
        sqla_session = db.session
        include_fk = True
    
class OrderReadSchema(schema.SQLAlchemySchema):
    payment_mode = fields.Integer(required=True)
    created_on = fields.DateTime(required=True)
    order_item = fields.Nested(OrderItemReadSchema,many=True)
    customer = fields.Nested(CustomerReadSchema,many=False,exclude=['password'])
    address = fields.Nested(CustomerAddressReadSchema,many=False)
    seller = fields.Nested(SellerReadSchema,many=False,exclude=['password'])
    
    class Meta:
        model=Order
        load_instance = True
        sqla_session = db.session
        include_fk = True