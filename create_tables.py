from db import Base, engine
import player, spin

Base.metadata.create_all(engine)