import uuid

class Player():
    def __init__(self, id = str(uuid.uuid4()), balance = 1000, bet_size = 40, last_win = 0):
        self.id = id
        self.balance = balance
        self.bet_size = bet_size
        self.last_win = last_win

    def bet(self, bet_size):
        if bet_size <= self.balance:
            self.bet_size = bet_size
            self.balance -= self.bet_size
        else:
            raise ValueError("Insufficient Balance")

    

