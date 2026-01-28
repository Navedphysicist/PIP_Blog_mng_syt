from fastapi import APIRouter,Depends,HTTPException, Query
from schema import BlogCreate,BlogDisplay
from db.database import get_db
from sqlalchemy.orm import Session
from models import DbBlog,DbUser
from typing import List

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

#POST
@router.post("",response_model=BlogDisplay)
def create_blog(blog:BlogCreate,user_id:int = Query(..., description = "Id of the user to create blog"), db:Session = Depends(get_db)):
    
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404,detail= "USER NOT FOUND")
    
    new_blog = DbBlog(
        title=blog.title,
        content = blog.content,
        user_id = user_id
        )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

#GET
@router.get("",response_model=List[BlogDisplay])
def get_all_blogs(user_id:int = Query(..., description = "Id of the user to create blog"),db:Session = Depends(get_db)):
    
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404,detail= "USER NOT FOUND")
    
    blogs = db.query(DbBlog).filter(DbBlog.user_id == user_id).all()
    return blogs
    
    
#GET - Single
@router.get("/{id}",response_model=BlogDisplay)
def get_blog(id:int,user_id:int = Query(..., description = "Id of the user to create blog"), db:Session = Depends(get_db)):
    
    user = db.query(DbUser).filter(DbUser.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404,detail= "USER NOT FOUND")
    
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=404, detail="Blog Not Found")
    
    if blog.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only access your own blogs")
 
    return blog

#PUT
@router.put("/{id}")
def update_blog(id:int,blog:BlogCreate,user_id:int = Query(..., description = "Id of the user to create blog"), db:Session = Depends(get_db)):
    ext_blog = db.query(DbBlog).filter(DbBlog.id == id).first()
    
    if not ext_blog:
        raise HTTPException(status_code=404,detail="Blog Not Found")
    
    if ext_blog.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can't edit other's blog")
    
    ext_blog.title = blog.title
    ext_blog.content = blog.content
    
    db.commit()
    db.refresh(ext_blog)
    
    return ext_blog



@router.delete("/{id}")
def delete_blog(id: int, user_id: int = Query(..., description="ID of the user deleting the blog"), db: Session = Depends(get_db)):
    blog = db.query(DbBlog).filter(DbBlog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404, detail="Blog Not Found")

    # Verify that the user is the creator of the blog
    if blog.user_id != user_id:
        raise HTTPException(
            status_code=403, detail="You can only delete your own blogs")

    db.delete(blog)
    db.commit()

    return {"message": "Blog deleted Succesfully!"}

