import os
from flask_restful import Resource
from flask import request
from flask import make_response
from flasgger import swag_from

from models.database import db
from models.seller.product import Product
from utils.error_handler import error_handler
from schemas.seller.product import ProductCreateSchema
from services.product_service import ProductService
from utils.jwt import validate_token
from swagger.swagger import route

class ProductCustomerView(Resource):
    product_service=ProductService()
    db_session=db.session
    
    @swag_from(os.path.join(route,'seller/get_products.yml'))
    @validate_token
    @error_handler
    def get(self):
        return self.product_service.get_all_products()

class ProductSellerView(Resource):
    product_service=ProductService()
    db_session=db.session
    
    @swag_from(os.path.join(route,'seller/add_product.yml'))
    @validate_token
    @error_handler
    def post(self):
        data=request.get_json()
        data['seller_id'] = request.user.id
        error=ProductCreateSchema().validate(data,session=self.db_session)
        if error:
            return make_response({"status":False,"detail":error},400)
        product=ProductCreateSchema().load(data,session=self.db_session)
        return self.product_service.create_product(product)
    
    @swag_from(os.path.join(route,'seller/get_products.yml'))
    @validate_token
    @error_handler
    def get(self):
        return self.product_service.get_my_products()

class ProductDetailView(Resource):
    product_service=ProductService()
    db_session=db.session
    
    @validate_token
    @error_handler
    def get(self,id):
        return self.product_service.get_product_detail(id)
    
    @swag_from(os.path.join(route,'seller/edit_product.yml'))
    @validate_token
    @error_handler
    def put(self,id):
        data=request.get_json()
        product=Product.query.get_or_404(id)
        if product.seller_id==None:
            return make_response({"status":False,"detail":"Can't edit unknown's product"},200)
        if request.user.id!=product.seller_id:
            return make_response({"status":False,"detail":"Can't edit other seller's product"},200)
        error=ProductCreateSchema().validate(data,session=self.db_session)
        if error:
            return make_response({"status":False,"detail":error},400)
        product=ProductCreateSchema().load(data,session=self.db_session,instance=product)
        return self.product_service.edit_product()
    
    @swag_from(os.path.join(route,'seller/delete_product.yml'))
    @validate_token
    @error_handler
    def delete(self,id):
        product=Product.query.get_or_404(id)
        if request.user.id!=product.seller_id:
            return make_response({"status":False,"detail":"Can't delete other seller's product"},400)
        return self.product_service.delete_product(product)