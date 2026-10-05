import uuid
from db import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

class PlayerError(Exception):
    """Base class for every player rule being broken"""

class NotEnoughBalance(PlayerError):
    pass

class BetNotAllowed(PlayerError):
    pass

class Player(Base):
    __tablename__ = 'players'
    player_id = Column('id', String, primary_key=True, nullable=False)
    balance = Column(Integer, nullable=False)
    bet_size = Column(Integer, nullable=False)
    last_win = Column(Integer, nullable=False)
    screen = Column(JSONB, nullable=False)

    spins = relationship('Spin', back_populates='player') 

    start_balance = 1000
    start_bet = 40
    start_win = 0
    allowed_bets = (10, 20, 40, 80, 120)
    start_screen = [
            ["🍉", "🍉", "🍉"],
            ["🍇", "🍇", "🍇"],
            ["🍋", "🍋", "🍋"],
            ["🍊", "🍊", "🍊"],
            ["🍒", "🍒", "🍒"],
        ]

    @classmethod
    def make_player(cls) -> Player:
        return cls(player_id = str(uuid.uuid4()), balance = cls.start_balance, bet_size = cls.start_bet, last_win = cls.start_win, screen = cls.start_screen)

    def pay_bet(self):
        if self.bet_size > self.balance:
            raise NotEnoughBalance()
        self.balance -= self.bet_size

    def collect_wins(self, winnings: int):
        if winnings > 0:
            self.balance += winnings
            self.last_win = winnings

    def change_bet_size(self, bet_size: int):
        if bet_size not in self.allowed_bets:
            raise BetNotAllowed()
        self.bet_size = bet_size
        
    def reset_balance(self):
        self.balance = self.start_balance

    @property
    def id(self):
        return self.player_id
