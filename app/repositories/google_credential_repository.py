import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.google_credential import GoogleCredential
from app.utils.crypt import encrypt, decrypt

class GoogleCredentialRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def create_google_credential(self,  user_id: int, token: dict,):

        token_json = json.dumps(token)
        encrypted_token = encrypt(token_json).decode()

        new_credential = GoogleCredential(user_token=encrypted_token, user_id=user_id)
        self.db.add(new_credential)
        self.db.commit()
        self.db.refresh(new_credential)
        
        return new_credential.to_dict() 


    def get_google_credential_by_user_id(self, user_id:int):
        response = self.db.query(GoogleCredential).filter(GoogleCredential.user_id == user_id).first()
    
        if not response:
            return None
        
        response_dict = response.to_dict() 
        cred_string = decrypt(response_dict["user_token"])
        return json.loads(cred_string)
    
    def update_user_token(self, user_id:int, token: dict):
        token_json = json.dumps(token)
        encrypted_token = encrypt(token_json).decode()
        
        self.db.query(GoogleCredential).filter(GoogleCredential.user_id == user_id).update(
            {"user_token": encrypted_token, "updated_at": datetime.utcnow()})
        self.db.commit()
        
        return True;
