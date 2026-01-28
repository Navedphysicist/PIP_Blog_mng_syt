from pydantic import BaseModel
from typing import Optional

# Schema for Incoming requests
class BlogCreate(BaseModel):
    title: str
    content: str
    
# Schema for Outgoing response

class BlogDisplay(BaseModel):
    id: int
    title:str
    content: str
    
    class Config:
        from_attributes = True
        
        
# AI Chat Schema
class ChatRequest(BaseModel):
    question : str
    
class ChatResponse(BaseModel):
    response: str
    
    
# User Schemas
class UserCreate(BaseModel):
    username:str
    email:str

class UserDisplay(BaseModel):
    id:int
    username:str
    email:str
    
    class Config:
        from_attributes = True
    