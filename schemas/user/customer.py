from schemas.schema import schema
from marshmallow import fields

from models.database import db
from models.user.customer import Customer

class CustomerCreateSchema(schema.SQLAlchemySchema):
    name=fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model=Customer
        load_instance=True

class CustomerReadSchema(schema.SQLAlchemyAutoSchema):
    name=fields.String(required=True)
    address=fields.String(required=True)
    email = fields.Email(required=True)
    phone_number = fields.String(required=False)
    password = fields.String(required=False)
    
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session
        include_fk = True