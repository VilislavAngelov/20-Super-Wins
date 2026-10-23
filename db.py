from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DB_URL

engine = create_engine(DB_URL)

SessionLocal = sessionmaker(bind=engine)

def get_session():
    with SessionLocal() as session:
        yield session

Base = declarative_base()