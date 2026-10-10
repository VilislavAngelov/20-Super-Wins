from player import Player, PlayerError
from dataclasses import dataclass
from spin import Spin

class PlayerNotFound(PlayerError):
    pass

@dataclass
class Outcome:
    screen: list[list[str]]
    winnings: int
    balance: int
    last_win: int
    spin_balance: int
    wins: list[dict]

class CasinoService:
    def __init__(self, session, machine):
        self.session = session
        self.machine = machine

    def spin(self, player_id):
        player = self._load_player(player_id)
        player.pay_bet()
        spin_balance = player.balance
        result = self.machine.spin()
        player.collect_wins(result.winnings)
        player.screen = result.screen
        
        player.spins.append(Spin(screen=result.screen, winnings=result.winnings, cost=player.bet_size))

        self.session.commit()
        return Outcome(screen=result.screen, winnings=result.winnings, balance=player.balance, last_win=player.last_win, spin_balance=spin_balance, wins=result.wins)

    def _load_player(self, player_id):
        player = self.session.get(Player, player_id) if player_id else None

        if player is None:
            raise PlayerNotFound()
        
        return player
            