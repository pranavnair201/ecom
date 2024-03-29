import os
from flask import Flask,render_template
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
from swagger.swagger import swag

app=Flask(__name__)
app.app_context().push()

api=Api(app)
CORS(app)

# app.config['AUTHY_API_KEY']=os.environ.get('AUTHY_API_KEY')

app.config['SQLALCHEMY_DATABASE_URI']="postgresql://ecom_admin:password@localhost:5432/ecom"#os.environ.get('SQLALCHEMY_DATABASE_URI')#"postgresql://ecom_admin:password@localhost:5432/ecom"

# Swagger configs
app.config["SWAGGER"] = {
    'title': "Ecom",
    'specs_route': '/swagger',
    "uiversion": 3,
}

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

with app.app_context():
    db.init_app(app)

schema.init_app(app)
swag.init_app(app)

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