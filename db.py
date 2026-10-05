from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql+psycopg://vili@/casino', echo=True)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()