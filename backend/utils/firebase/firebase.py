
# import firebase_admin
# import pyrebase
# import json
# from firebase_admin import credentials, auth
# from flask import make_response

# class FirebaseHandler():
#     cred=None
#     firebase=None
#     pb=None
    
#     def __init__(self):
#         self.cred = credentials.Certificate('fb_admin_creds.json')
#         self.firebase = firebase_admin.initialize_app(self.cred)
#         self.pb = pyrebase.initialize_app(json.load(open('fb_app_creds.json')))
    
#     def create_uid(self,data):
#         email=data.get('email',None)
#         password=data.get('password',None)
#         phone_number=data.get('phone_number',None)
        
#         if bool(email) and bool(password):
#             user = auth.create_user(
#                 email=email,
#                 password=password
#             )
#         elif bool(phone_number):
#             user = auth.create_user(
#                 phone_number=phone_number
#             )
#         return user.uid
            