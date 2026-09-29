import uuid

class PlayerError(Exception):
    """Base class for every player rule being broken"""

class NotEnoughBalance(PlayerError):
    pass

class BetNotAllowed(PlayerError):
    pass

class Player():

    start_balance = 1000
    start_bet = 40
    last_win = 0
    allowed_bets = (10, 20, 40, 80, 120)
    start_screen = [
            ["🍉", "🍉", "🍉"],
            ["🍇", "🍇", "🍇"],
            ["🍋", "🍋", "🍋"],
            ["🍊", "🍊", "🍊"],
            ["🍒", "🍒", "🍒"],
        ]

    def __init__(self, id: str, balance: int, bet_size: int, last_win: int, screen: list[list[str]]):
        self._id = id
        self.balance = balance
        self.bet_size = bet_size
        self.last_win = last_win
        self.screen = screen

    @classmethod
    def make_player(cls) -> Player:
        return cls(id = str(uuid.uuid4()), balance = cls.start_balance, bet_size = cls.start_bet, last_win = cls.last_win, screen = cls.start_screen)

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
        return self._id
