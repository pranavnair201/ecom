from models.database import db
from models.orders.order_item import OrderItem

class Product(db.Model):
    __tablename__='product'
    id=db.Column(db.Integer,primary_key=True)
    seller_id=db.Column(db.String(50),db.ForeignKey('seller.uid'))
    name=db.Column(db.String(30),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    order_item = db.relationship(OrderItem,backref='product')
    
    def __repr__(self):
        return f"{self.name}"