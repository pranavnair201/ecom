import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS 
from flask_migrate import Migrate
from flask_mail import Mail

from schemas.schema import schema
from apis.user import UserCreateView,UserLoginView,UserVerifyView
from apis.product import ProductDetailView,ProductSellerView,ProductCustomerView
from apis.customer_address import CustomerAddressView,CustomerAddressDetailView,StateView,DistrictView
from apis.order import OrderCustomerView,OrderSellerView,SellerEarningView
from models.database import db
from utils.mail_handler import mail

app=Flask(__name__)

api=Api(app)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']="postgresql://ecom_admin:password@localhost:5432/ecom"


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)
db.init_app(app)
schema.init_app(app)

migrate=Migrate(app,db)

api.add_resource(UserCreateView, '/user')
api.add_resource(UserLoginView, '/user/login')
api.add_resource(UserVerifyView, '/user/verify')

api.add_resource(ProductSellerView, '/product')
api.add_resource(ProductCustomerView, '/home')
api.add_resource(ProductDetailView, '/product/<int:id>')

api.add_resource(CustomerAddressView, '/customer_address')
api.add_resource(CustomerAddressDetailView, '/customer_address/<int:id>')
api.add_resource(StateView, '/state')
api.add_resource(DistrictView, '/district')

api.add_resource(OrderCustomerView,'/order')
api.add_resource(OrderSellerView,'/seller-order')
api.add_resource(SellerEarningView,'/seller-earning')

if __name__=='__main__':
    app.debug=True
    app.run(host="0.0.0.0")