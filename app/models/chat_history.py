from app.utils.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Text

class ChatHistory(Base):
    __tablename__ = "chat_histories"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    parent_chat_id = Column(Integer, ForeignKey('chat_histories.id',ondelete="CASCADE"), nullable=True) # if null means it is a query from user #
    message = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=True) # if null means chat bot replied #
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="google_credentials")
    parent_chat = relationship("ParentChat", back_populates="chat_histories")
    
    def to_dict(self):
        return {
            "id": self.id,
            "parent_chat_id": self.parent_chat_id,
            "message": self.message,
            "user_id" : self.user_id,
            "created_at": self.created_at.isoformat()  
        }