import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, future=True, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
