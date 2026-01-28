from fastapi import FastAPI
from db.database import Base,engine
from routers import blog,ai_chat,user,handle_file
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Blog Management System"
)

Base.metadata.create_all(bind=engine)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(handle_file.router)
app.include_router(ai_chat.router)

app.mount("/files",StaticFiles(directory="files"),name="files")

@app.get("/")
def root():
    return {
        "message" : "Welcome to Blog Management System",
        "status" : "App is running..."
    }