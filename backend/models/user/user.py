from models.database import db

class User(db.Model):
    __abstract__=True
    email=db.Column(db.String(30),unique=True,nullable=True)
    phone_number=db.Column(db.String(15),unique=True,nullable=True)
    password = db.Column(db.String(100),nullable=True)
    is_verified=db.Column(db.Boolean,default=False)