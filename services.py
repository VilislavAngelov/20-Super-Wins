from player import Player, PlayerError
from dataclasses import dataclass
from spin import Spin

class PlayerNotFound(PlayerError):
    status_code = 401
    detail = "No player session found"

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

    def _load_player(self, player_id, lock=False):
        player = self.session.get(Player, player_id, with_for_update=lock) if player_id else None
        if player is None:
            raise PlayerNotFound()
        
        return player

    def get_or_create_player(self, player_id):
        player = self.session.get(Player, player_id) if player_id else None
        if player is None:
            player = Player.make_player()
            self.session.add(player)
            self.session.commit()
        
        return player
    
    def spin(self, player_id):
        player = self._load_player(player_id, lock=True)
        player.pay_bet()
        spin_balance = player.balance
        result = self.machine.spin()
        player.collect_wins(result.winnings)
        player.screen = result.screen
        
        player.spins.append(Spin(screen=result.screen, winnings=result.winnings, cost=player.bet_size))

        self.session.commit()

        return Outcome(screen=result.screen, winnings=result.winnings, balance=player.balance, last_win=player.last_win, spin_balance=spin_balance, wins=result.wins)

    def player_reset_balance(self, player_id):
        player = self._load_player(player_id, lock=True)
        player.reset_balance()

        self.session.commit()
        return player.balance

    def player_change_bet(self, player_id, bet_size):
        player = self._load_player(player_id, lock=True)
        player.change_bet_size(bet_size)

        self.session.commit()
        return player.bet_size

    def player_history(self, player_id):
        self._load_player(player_id)

        spins = (
            self.session.query(Spin)
            .filter(Spin.player_id == player_id)
            .order_by(Spin.spin_id.desc())
            .limit(100)
            .all()
        )
        return [
            {"screen": s.screen, "winnings": s.winnings, "cost": s.cost, "at": s.timestamp}
            for s in spins
        ]