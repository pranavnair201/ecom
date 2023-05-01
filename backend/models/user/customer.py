from models.database import db
from models.user.user import User
from models.customer.customer_address import CustomerAddress
from models.orders.order import Order

class CustomerProfile(User):
    __tablename__='customer'
    uid=db.Column(db.String(50),primary_key=True)
    name=db.Column(db.String(30),unique=False,nullable=False)
    addresses = db.relationship(CustomerAddress,backref='customer',cascade='all, delete',single_parent=True, lazy='dynamic')
    order = db.relationship(Order,backref='customer')
    
    def __repr__(self):
        return f"{self.name}"