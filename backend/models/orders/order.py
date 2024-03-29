import enum
from sqlalchemy_utils import aggregated
from datetime import datetime


from models.database import db
from models.orders.order_item import OrderItem


class PaymentModeEnum(enum.IntEnum):
    COD=1
    ONLINE=2

class Order(db.Model):
    __tablename__='order_table'
    id=db.Column(db.Integer,primary_key=True)
    customer_id=db.Column(db.String(50),db.ForeignKey('customer.uid'))
    customer_address_id=db.Column(db.Integer,db.ForeignKey('address.id'))
    seller_id=db.Column(db.String(50),db.ForeignKey('seller.uid'))
    payment_mode=db.Column(db.Enum(PaymentModeEnum),default=PaymentModeEnum.COD,nullable=False)
    created_on=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    order_item = db.orm.relationship(OrderItem,backref='order_table',cascade='all, delete-orphan',single_parent=True, lazy='dynamic')
    
    def __init__(self,data):
        self.customer_id=data.get('customer_id',None)
        self.customer_address_id=data.get('customer_address_id',None)
        self.seller_id=data.get('seller_id',None)
        self.payment_mode=data.get('payment_mode',None)
    
    # @aggregated('order_item', db.Column(db.Integer))
    # def total(self):
    #     return db.func.sum(OrderItem.rate)