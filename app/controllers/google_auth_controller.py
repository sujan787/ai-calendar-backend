import cherrypy
from app.services.google_auth_service import GoogleAuthService
from app.repositories.google_credential_repository import GoogleCredentialRepository
from app.repositories.user_repository import UserRepository
from app.utils.database import db_transaction, db_query
from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_CALENDAR_SCOPE
from app.tools.auth import create_jwt_token, use_auth

use_auth()
class GoogleAuthController:
    
    def __init__(self):
        self.google_auth_service = GoogleAuthService()

   
    @cherrypy.expose("profile")
    @cherrypy.tools.json_out()
    def profile_login(self,**param):
        cherrypy.session['redirect'] =  param.get("redirect", None)
        raise cherrypy.HTTPRedirect(self.google_auth_service.get_google_auth_url("PROFILE"))
   

    @cherrypy.expose("calendar")
    @cherrypy.tools.auth()
    def calendar_login(self, **param):
        user = cherrypy.request.user
        cherrypy.session['redirect'] = param.get("redirect", None)
        cherrypy.session['user'] = user
        raise cherrypy.HTTPRedirect(self.google_auth_service.get_google_auth_url("CALENDAR"))
    
    @cherrypy.expose("callback")
    def oauth_callback(self, **param):
        token = self.google_auth_service.retrieve_token(param["code"])
        
        if token["scope"] == GOOGLE_CALENDAR_SCOPE: 
            user = cherrypy.session.pop('user', None);
            google_credential = db_query(lambda db: 
                (GoogleCredentialRepository(db)).get_google_credential_by_user_id(user["id"])
            )
            
            credential = {
                    "token": token["access_token"],
                    "refresh_token": token["refresh_token"],
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "scopes": [token["scope"]]
            }
            
            if google_credential:
                db_transaction(lambda db: 
                    GoogleCredentialRepository(db).update_user_token(user["id"], credential)
                )
            else:
                db_transaction(lambda db: 
                    GoogleCredentialRepository(db).create_google_credential( user["id"], credential)
                )
            
        else:
            profile = self.google_auth_service.fetch_profile(token)
            
            user = db_query(lambda db: (UserRepository(db)).get_user_by_email(profile["email"]))
        
            user = user if user else db_transaction(lambda db: (UserRepository(db).create_user(
                profile["name"], profile["email"], profile["id"]
            )))
            
            jwt_token = create_jwt_token(user)
            
            cherrypy.response.cookie["auth_token"] = jwt_token
            cherrypy.response.cookie["auth_token"]["path"] = "/"
            cherrypy.response.cookie["auth_token"]["secure"] = cherrypy.request.scheme == "https"
            cherrypy.response.cookie["auth_token"]["httponly"] = True  
            cherrypy.response.cookie["auth_token"]["max-age"] = 3600

        redirect_url = cherrypy.session.pop('redirect', None);
        
        raise cherrypy.HTTPRedirect(redirect_url)
    
    @cherrypy.expose("login_user")
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def login_user(self):
        user = cherrypy.request.user 
        if user:
            cherrypy.response.status = 200
            return user; 
        else:
            cherrypy.response.status = 400
            return {"error" : "user not found"};
        
        
    @cherrypy.expose("calendar_status")
    @cherrypy.tools.json_out()
    @cherrypy.tools.auth()
    def calendar_status(self):
        user = cherrypy.request.user 
        credentials = db_query(lambda db: 
            (GoogleCredentialRepository(db)).get_google_credential_by_user_id(user["id"])
        )
        
        return {"status" : bool(credentials)}   