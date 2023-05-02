import os
from twilio.rest import Client
# from authy.api import AuthyApiClient

# phone_auth = AuthyApiClient(os.environ.get('AUTHY_API_KEY'))
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
phone_auth = Client(account_sid, auth_token)

service = phone_auth.verify.v2.services.create(friendly_name='My Verify Service')