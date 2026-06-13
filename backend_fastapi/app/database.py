import os
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# Absolute path to SQLite DB (placed in repository root)
BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = os.path.join(BASE_DIR, "data.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    free_interviews = Column(Integer, default=1)
    is_premium = Column(Boolean, default=False)
    history = Column(Text)  # JSON string of past interviews

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
