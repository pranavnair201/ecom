from flask import make_response,request
from flask_restful import Resource

from utils.jwt import validate_token
from utils.error_handler import error_handler
from services.order_service import OrderService

class OrderCustomerView(Resource):
    order_service=OrderService()
    
    @validate_token
    @error_handler
    def post(self):
        data=request.get_json()
        data['customer_id'] = request.user.id
        return self.order_service.create_order(data)
    
    @validate_token
    @error_handler
    def get(self):
        return self.order_service.get_customer_my_orders()

class OrderSellerView(Resource):
    order_service=OrderService()
    
    @validate_token
    @error_handler
    def get(self):
        return self.order_service.get_seller_my_orders()

class SellerEarningView(Resource):
    order_service=OrderService()
    
    @validate_token
    @error_handler
    def get(self):
        args=request.args.to_dict()
        start_date=args.get('start_date',None)
        end_date=args.get('end_date',None)
        return self.order_service.get_seller_earning(start_date,end_date)