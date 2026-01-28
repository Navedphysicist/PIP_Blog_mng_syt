from sqlalchemy import Column, Integer, String,ForeignKey
from db.database import Base
from sqlalchemy.orm import relationship

class DbBlog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    
    #Foreign Key
    user_id = Column(Integer,ForeignKey("users.id"), nullable=False)
    
    #Relationship
    user = relationship("DbUser", back_populates="blogs")
    
class DbUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,nullable=False,unique=True)
    email = Column(String,nullable=False)
    
    #Relationship
    blogs = relationship("DbBlog", back_populates="user")
    
