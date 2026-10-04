from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql+psycopg://vili@/casino', echo=True)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()