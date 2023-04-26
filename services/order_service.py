from flask import make_response,request
from sqlalchemy import and_

from schemas.order.order import OrderSchema,OrderItemSchema,OrderReadSchema,OrderItemReadSchema
from models.database import db
from models.orders.order import Order
from models.orders.order_item import OrderItem
from models.seller.product import Product

class OrderService():
    db_session=db.session
    
    def get_seller_earning(self,start_date,end_date):
        query=Order.query.filter(
            and_(Order.created_on>=start_date,Order.created_on<=end_date)
        )
        total=0
        for order in query:
            total+=order.total
        earnings_data={"earning":total}
        return make_response({"status":True,"detail":earnings_data},200)
    
    def get_seller_my_orders(self):
        orders=Order.query.filter_by(seller_id=request.user.id)
        orders_data=OrderReadSchema(exclude=['seller']).dump(orders,many=True)
        return make_response({"status":True,"detail":orders_data},200)
    
    def get_customer_my_orders(self):
        orders=Order.query.filter_by(customer_id=request.user.id)
        orders_data=OrderReadSchema(exclude=['customer']).dump(orders,many=True)
        return make_response({"status":True,"detail":orders_data},200)

    
    def create_order_items(self,data,order_id):
        for item in data:
            item['order_id']=order_id
            error=OrderItemSchema().validate(item,session=self.db_session)
            if error:
                Order.query.get(order_id).delete()
                return make_response({"status":False,"detail":error},400)
            order_item=OrderItem(item)
            self.db_session.add(order_item)
            product=Product.query.get(order_item.product_id)
            product.quantity-=order_item.quantity
        self.db_session.commit()
        return make_response({"status":True,"detail":"Order created successfully..!!"},200)
    
    def create_order(self,data):
        error=OrderSchema().validate(data,session=self.db_session)
        if error:
            return make_response({"status":False,"detail":error},400)
        order=Order(data)
        self.db_session.add(order)
        self.db_session.commit()
        return self.create_order_items(data.get('order_items',None),order.id)
        