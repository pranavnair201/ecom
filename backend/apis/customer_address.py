import os
from flask_restful import Resource
from flask import request
from flask import make_response
from flasgger import swag_from

from models.database import db
from models.customer.customer_address import CustomerAddress
from utils.error_handler import error_handler
from schemas.customer.customer_address import CustomerAddressCreateSchema,StateCreateSchema,DistrictCreateSchema
from services.customer_address_service import CustomerAddressService,StateService,DistrictService
from utils.jwt import validate_token
from swagger.swagger import route


class CustomerAddressView(Resource):
    customer_address_service=CustomerAddressService()
    db_session=db.session
    
    @swag_from(os.path.join(route,'customer/add_address.yml'))
    @validate_token
    @error_handler
    def post(self):
        data=request.get_json()
        data['customer_id'] = request.user.uid
        error=CustomerAddressCreateSchema().validate(data,session=self.db_session)
        if error:
            return make_response({"status":False,"detail":error},400)
        customer_address=CustomerAddressCreateSchema().load(data,session=self.db_session)
        return self.customer_address_service.create_customer_address(customer_address)
    
    @swag_from(os.path.join(route,'customer/get_address.yml'))
    @validate_token
    @error_handler
    def get(self):
        return self.customer_address_service.get_my_customer_addresss()

class CustomerAddressDetailView(Resource):
    customer_address_service=CustomerAddressService()
    db_session=db.session
    
    @validate_token
    @error_handler
    def get(self,id):
        return self.customer_address_service.get_customer_address_detail(id)
    
    @validate_token
    @error_handler
    def put(self,id):
        data=request.get_json()
        customer_address=CustomerAddress.query.get_or_404(id)
        if customer_address.customer_id==None:
            return make_response({"status":False,"detail":"Can't edit unknown's customer_address"},200)
        if request.user.uid!=customer_address.customer_id:
            return make_response({"status":False,"detail":"Can't edit other customer's customer_address"},200)
        error=CustomerAddressCreateSchema().validate(data,session=self.db_session)
        if error:
            return make_response({"status":False,"detail":error},400)
        customer_address=CustomerAddressCreateSchema().load(data,session=self.db_session,instance=customer_address)
        return self.customer_address_service.edit_customer_address()
    
    @validate_token
    @error_handler
    def delete(self,id):
        customer_address=CustomerAddress.query.get_or_404(id)
        if request.user.uid!=customer_address.customer_id:
            return make_response({"status":False,"detail":"Can't delete other customer's customer_address"},400)
        return self.customer_address_service.delete_customer_address(customer_address)


class StateView(Resource):
    state_service=StateService()
    db_session=db.session
    
    @validate_token
    @error_handler
    def post(self):
        data=request.get_json()
        error=StateCreateSchema().validate(data,session=self.db_session)
        if error:
            return make_response({"status":False,"detail":error},400)
        state=StateCreateSchema().load(data,session=self.db_session)
        return self.state_service.create_state(state)
    
    @validate_token
    @error_handler
    def get(self):
        return self.state_service.get_all_state()

class DistrictView(Resource):
    district_service=DistrictService()
    db_session=db.session
    
    @validate_token
    @error_handler
    def post(self):
        data=request.get_json()
        error=DistrictCreateSchema().validate(data,session=self.db_session)
        if error:
            return make_response({"status":False,"detail":error},400)
        district=DistrictCreateSchema().load(data,session=self.db_session)
        return self.district_service.create_district(district)
    
    @validate_token
    @error_handler
    def get(self):
        args=request.args.to_dict()
        return self.district_service.get_all_district(int(args['state_id']))