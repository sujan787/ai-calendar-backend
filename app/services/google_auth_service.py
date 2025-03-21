from config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI, GOOGLE_CALENDAR_SCOPE, GOOGLE_PROFILE_SCOPE
from urllib.parse import urlencode, parse_qs
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.repositories.google_credential_repository import GoogleCredentialRepository
from app.utils.database import db_query, db_transaction

class GoogleAuthService:
    
    def get_google_auth_url(self, type: str):
        scope = {
            "CALENDAR": GOOGLE_CALENDAR_SCOPE,
            "PROFILE": GOOGLE_PROFILE_SCOPE
         }.get(type, GOOGLE_PROFILE_SCOPE)

        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": scope,
            "access_type": "offline",
            "prompt": "consent"
        }
        
        auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
        
        return auth_url;
    
    def retrieve_token(self, code: str):
        token_url = "https://oauth2.googleapis.com/token"
        
        data = {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": GOOGLE_REDIRECT_URI
        }
        
        response = requests.post(token_url, data=data).json()
        
        return response
    
    def fetch_profile(self, token_json:dict):
        user_info = requests.get(
            "https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {token_json['access_token']}"},
        ).json()
        
        return user_info
    
    def get_user_credentials(self, user_id: int):
         
        googleCredential = db_query(lambda db:
            (GoogleCredentialRepository(db)).get_google_credential_by_user_id(user_id)
        )
        
        credentials = Credentials.from_authorized_user_info(googleCredential)
        
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            
        return credentials