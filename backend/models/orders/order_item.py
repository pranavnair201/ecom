from models.database import db

class OrderItem(db.Model):
    __tablename__='order_item'
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey('order_table.id'))
    product_id=db.Column(db.Integer,db.ForeignKey('product.id'))
    quantity=db.Column(db.Integer,nullable=False)
    rate=db.Column(db.Integer,nullable=False)
    
    def __init__(self,data):
        self.order_id=data.get('order_id',None)
        self.product_id=data.get('product_id',None)
        self.quantity=data.get('quantity',None)
        self.rate=data.get('rate',None)