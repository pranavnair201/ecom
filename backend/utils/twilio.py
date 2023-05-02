import os
from twilio.rest import Client
# from authy.api import AuthyApiClient

# phone_auth = AuthyApiClient(os.environ.get('AUTHY_API_KEY'))
account_sid = "AC0a719bd300142a191cbb04e544a40266"#os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = "da2e2e50d2f8cd3f622c3bc6647409eb"#os.environ.get('TWILIO_AUTH_TOKEN')
phone_auth = Client(account_sid, auth_token)

service = phone_auth.verify.v2.services.create(friendly_name='My Verify Service')