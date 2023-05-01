
from models.database import db

from models.orders.order import Order

class CustomerAddress(db.Model):
    __tablename__='address'
    id=db.Column(db.Integer,primary_key=True)
    building=db.Column(db.String(30),nullable=False)
    street=db.Column(db.String(30),nullable=True)
    area=db.Column(db.String(30),nullable=False)
    district_id=db.Column(db.Integer,db.ForeignKey('district.id'))
    state_id=db.Column(db.Integer,db.ForeignKey('state.id'))
    customer_id=db.Column(db.String(50),db.ForeignKey('customer.uid'))
    order = db.relationship(Order,backref='address')
    
    def __repr__(self):
        return f"{self.customer}"

class District(db.Model):
    __tablename__='district'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    state_id=db.Column(db.Integer,db.ForeignKey('state.id'))
    address = db.relationship(CustomerAddress,backref='district',cascade='all, delete')
    
    def __repr__(self):
        return f"{self.name}"

class State(db.Model):
    __tablename__='state'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(30),nullable=False)
    district = db.relationship(District,backref='state',cascade='all, delete')
    address = db.relationship(CustomerAddress,backref='state',cascade='all, delete')
    
    def __repr__(self):
        return f"{self.name}"

