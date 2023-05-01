from flask import make_response

from flask import request
from schemas.customer.customer_address import CustomerAddressReadSchema,DistrictReadSchema,StateReadSchema
from models.database import db
from models.customer.customer_address import CustomerAddress
from models.customer.customer_address import State,District

class CustomerAddressService():
    db_session=db.session
    
    def create_customer_address(self,customer_address):
        self.db_session.add(customer_address)
        self.db_session.commit()
        return make_response({"status":True,"detail":"Customer address created successfully..!!"})
    
    def get_my_customer_addresss(self):
        customer_addresss=CustomerAddress.query.filter_by(customer_id=request.user.uid)
        customer_addresss_data=CustomerAddressReadSchema().dump(customer_addresss,many=True)
        return make_response({"status":True,"detail":customer_addresss_data},200)

    def get_customer_address_detail(self,id):
        customer_addresss=CustomerAddress.query.get_or_404(id)
        customer_addresss_data=CustomerAddressReadSchema().dump(customer_addresss,many=False)
        return make_response({"status":True,"detail":customer_addresss_data},200)
    
    def edit_customer_address(self):
        db.session.commit()
        return make_response({"status":True,"detail":"Edited successfully"},200)
    
    def delete_customer_address(self,customer_address):
        db.session.delete(customer_address)
        db.session.commit()
        return make_response({"status":True,"detail":"Deleted successfully"},200)

class StateService():
    db_session=db.session
    
    def create_state(self,state):
        self.db_session.add(state)
        self.db_session.commit()
        return make_response({"status":True,"detail":"State added successfully..!!"})
    
    def get_all_state(self):
        state=State.query.all()
        state_data=StateReadSchema().dump(state,many=True)
        return make_response({"status":True,"detail":state_data},200)

class DistrictService():
    db_session=db.session
    
    def create_district(self,state):
        self.db_session.add(state)
        self.db_session.commit()
        return make_response({"status":True,"detail":"District added successfully..!!"})
    
    def get_all_district(self,state_id=None):
        if state_id:
            district=District.query.filter_by(state_id=state_id)
        else:
            district=District.query.all()
        district_data=DistrictReadSchema().dump(district,many=True)
        return make_response({"status":True,"detail":district_data},200)