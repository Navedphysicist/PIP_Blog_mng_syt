from fastapi import APIRouter, Depends, HTTPException, Query
from schema import BlogCreate, BlogDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from models import DbBlog, DbUser
from typing import List

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

# POST


@router.post("", response_model=BlogDisplay)  # Create new blog endpoint
def create_blog(blog: BlogCreate, user_id: int = Query(..., description="Id of the user to create blog"), db: Session = Depends(get_db)):

    # Validate user exists before creating blog
    user = db.query(DbUser).filter(DbUser.id == user_id).first()

    if not user:
        # Return 404 if user doesn't exist
        raise HTTPException(status_code=404, detail="USER NOT FOUND")

    new_blog = DbBlog(
        title=blog.title,
        content=blog.content,
        user_id=user_id  # Associate blog with user via foreign key
    )

    db.add(new_blog)  # Add blog to database session
    db.commit()  # Persist changes to database
    db.refresh(new_blog)  # Refresh to get auto-generated ID
    return new_blog

# GET


@router.get("", response_model=List[BlogDisplay])  # Get all blogs for a user
def get_all_blogs(user_id: int = Query(..., description="Id of the user to create blog"), db: Session = Depends(get_db)):

    user = db.query(DbUser).filter(
        DbUser.id == user_id).first()  # Validate user exists

    if not user:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")

    # Filter blogs by user_id to return only user's blogs
    blogs = db.query(DbBlog).filter(DbBlog.user_id == user_id).all()
    return blogs


# GET - Single
@router.get("/{id}", response_model=BlogDisplay)  # Get single blog by ID
def get_blog(id: int, user_id: int = Query(..., description="Id of the user to create blog"), db: Session = Depends(get_db)):

    user = db.query(DbUser).filter(
        DbUser.id == user_id).first()  # Validate user exists

    if not user:
        raise HTTPException(status_code=404, detail="USER NOT FOUND")

    blog = db.query(DbBlog).filter(DbBlog.id == id).first()  # Query blog by ID

    if not blog:
        raise HTTPException(status_code=404, detail="Blog Not Found")

    if blog.user_id != user_id:  # Authorization check: users can only access their own blogs
        raise HTTPException(
            status_code=403, detail="You can only access your own blogs")

    return blog

# PUT


@router.put("/{id}")  # Update blog endpoint
def update_blog(id: int, blog: BlogCreate, user_id: int = Query(..., description="Id of the user to create blog"), db: Session = Depends(get_db)):
    ext_blog = db.query(DbBlog).filter(
        DbBlog.id == id).first()  # Find blog by ID

    if not ext_blog:
        raise HTTPException(status_code=404, detail="Blog Not Found")

    if ext_blog.user_id != user_id:  # Authorization check: only blog owner can update
        raise HTTPException(
            status_code=403, detail="You can't edit other's blog")

    ext_blog.title = blog.title  # Update blog title
    ext_blog.content = blog.content  # Update blog content

    db.commit()  # Persist changes to database
    db.refresh(ext_blog)  # Refresh to get updated data

    return ext_blog


@router.delete("/{id}")  # Delete blog endpoint
def delete_blog(id: int, user_id: int = Query(..., description="ID of the user deleting the blog"), db: Session = Depends(get_db)):
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()  # Find blog by ID

    if not blog:
        raise HTTPException(status_code=404, detail="Blog Not Found")

    if blog.user_id != user_id:  # Authorization check: only blog owner can delete
        raise HTTPException(
            status_code=403, detail="You can only delete your own blogs")

    db.delete(blog)  # Mark blog for deletion
    db.commit()  # Persist deletion to database

    return {"message": "Blog deleted Succesfully!"}
