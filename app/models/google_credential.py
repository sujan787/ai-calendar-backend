from app.utils.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Text
from app.models.user import User

class GoogleCredential(Base):
    __tablename__ = "google_credentials"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_token = Column(Text, nullable=False) # token should be encrypted #
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="google_credentials")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_token": self.user_token,
            "user_id" : self.user_id,
        }