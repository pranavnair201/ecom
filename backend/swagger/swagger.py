import os
from flasgger import Swagger

SWAGGER_TEMPLATE = {
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "token",
            "in": "header"
        }
    }
}

swag=Swagger(template=SWAGGER_TEMPLATE,)

route = os.path.abspath(os.path.dirname(__file__))