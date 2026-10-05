from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

class Spin(Base):
    __tablename__ = 'spins'
    spin_id = Column('id', Integer, primary_key=True, nullable=False)
    player_id = Column(String, ForeignKey('players.id'), nullable=False)
    screen = Column(JSONB, nullable=False)
    winnings = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    player = relationship('Player', back_populates='spins') 