from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./blog_mng.db"

# Create Engine => Database
engine = create_engine(DATABASE_URL,connect_args={"check_same_thread": False})

#Sessions
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base => To connect models
Base = declarative_base()

#Generator Function => Return session when called
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()