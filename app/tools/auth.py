import cherrypy
import jwt
import datetime
from config import APP_SECRET


def create_jwt_token(data):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = { **data,  "exp": expiration_time }

    return jwt.encode(payload, APP_SECRET, algorithm="HS256")

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, APP_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise cherrypy.HTTPError(401, "Token expired")
    except jwt.InvalidTokenError:
        raise cherrypy.HTTPError(401, "Invalid token")

def auth_middleware():
    if cherrypy.request.method == "OPTIONS": # to handle cors request
            cherrypy.response.status = 200
            cherrypy.response.body = b"ok"
            return 
        
    token_cookie = cherrypy.request.cookie.get("auth_token")
    token = token_cookie.value if token_cookie else None

    if not token:
        print(cherrypy.request.headers)
        token = cherrypy.request.headers.get("Auth-Token")

    if not token:
        raise cherrypy.HTTPError(401, "Missing token")

    try:
        user_data = verify_jwt_token(token)
        cherrypy.request.user = user_data
    except cherrypy.HTTPError as err:
        raise err  
    except Exception as e:
        raise cherrypy.HTTPError(401, f"Authentication error: {str(e)}")

def use_auth():
    cherrypy.tools.auth = cherrypy.Tool("before_handler", auth_middleware)        