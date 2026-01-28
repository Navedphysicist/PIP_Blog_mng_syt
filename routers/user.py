from fastapi import APIRouter, Depends, HTTPException, Query
from schema import UserCreate, UserDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from models import DbUser
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Response model ensures output matches UserDisplay schema
@router.post("", response_model=UserDisplay)
# Database session injected via dependency injection
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(DbUser).filter(
        # Check if username already exists
        DbUser.username == user.username).first()

    if existing_user:
        # Prevent duplicate usernames
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = DbUser(
        username=user.username,
        email=user.email
    )

    db.add(new_user)  # Add new user to database session
    db.commit()  # Persist changes to database
    db.refresh(new_user)  # Refresh to get auto-generated ID and other fields
    return new_user


# Response model ensures list of UserDisplay objects
@router.get("", response_model=List[UserDisplay])
# Database session injected via dependency injection
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(DbUser).all()  # Query all users from database
    return users
