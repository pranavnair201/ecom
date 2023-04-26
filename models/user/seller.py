from models.database import db
from models.user.user import User
from models.seller.product import Product
from models.orders.order import Order

class Seller(User):
    __tablename__='seller'
    id=db.Column(db.Integer,primary_key=True)
    shop_name=db.Column(db.String(30),nullable=False, unique=False)
    address=db.Column(db.String(30),nullable=False, unique=False)
    products = db.relationship(Product,backref='seller',cascade='all, delete',single_parent=True, lazy='dynamic')
    order = db.relationship(Order,backref='seller')
    