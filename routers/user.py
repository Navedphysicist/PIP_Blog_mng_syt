from fastapi import APIRouter,Depends,HTTPException, Query
from schema import UserCreate,UserDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from models import DbUser
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("",response_model=UserDisplay)
def create_user(user:UserCreate,db:Session = Depends(get_db)):
    
    existing_user = db.query(DbUser).filter(DbUser.username == user.username).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    new_user = DbUser(
        username=user.username,
        email = user.email
    )
        
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("",response_model=List[UserDisplay])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(DbUser).all()
    return users