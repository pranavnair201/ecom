import os
from authy.api import AuthyApiClient

phone_auth = AuthyApiClient(os.environ.get('AUTHY_API_KEY'))