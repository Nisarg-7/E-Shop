from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_url = "postgresql://app_45n0_user:bwTFSxzAVNKqJAI3qEbMzX6gh16Lw5FQ@dpg-d48su16r433s73a9707g-a.oregon-postgres.render.com/app_45n0"

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()