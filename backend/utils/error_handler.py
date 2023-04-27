from flask import make_response,request

def error_handler(func):
    
    def wrapper(*args, **kwargs):
        try:
            app = request.headers['app']
        except Exception as e:
            return make_response({"message": "App not provided"}, 403)
        if app not in ['seller','customer']:
            return make_response({"message": "App is invalid"}, 403)
        request.app=app
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return make_response({"status":False,"detail": str(e)}, 400)
    return wrapper