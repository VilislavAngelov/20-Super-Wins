from db import Base, engine
import player

Base.metadata.create_all(engine)