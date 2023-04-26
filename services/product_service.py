from flask import make_response

from flask import request
from schemas.seller.product import ProductReadSchema
from models.database import db
from models.seller.product import Product

class ProductService():
    db_session=db.session
    
    def create_product(self,product):
        self.db_session.add(product)
        self.db_session.commit()
        return make_response({"status":True,"detail":"Product created successfully..!!"})
    
    def get_all_products(self):
        products=Product.query.all()
        products_data=ProductReadSchema().dump(products,many=True)
        return make_response({"status":True,"detail":products_data},200)

    def get_my_products(self):
        products=Product.query.filter_by(seller_id=request.user.id)
        products_data=ProductReadSchema().dump(products,many=True)
        return make_response({"status":True,"detail":products_data},200)

    def get_product_detail(self,id):
        products=Product.query.get_or_404(id)
        products_data=ProductReadSchema().dump(products,many=False)
        return make_response({"status":True,"detail":products_data},200)
    
    def edit_product(self):
        db.session.commit()
        return make_response({"status":True,"detail":"Edited successfully"},200)
    
    def delete_product(self,product):
        db.session.delete(product)
        db.session.commit()
        return make_response({"status":True,"detail":"Deleted successfully"},200)
    