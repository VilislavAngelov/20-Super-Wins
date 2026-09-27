import random
from dataclasses import dataclass

@dataclass(frozen=True)
class SpinResult:
    screen: list[list[str]]
    winnings: int
    wins: list[object]


class SlotMachine:

    lines_payouts = {5 : 50, 4 : 10, 3 : 5}
    symbols_multiplier = {
        "🍋": 1,
        "🍒": 1,
        "🍊": 2,
        "🍉": 2,
        "🍇": 3,
        "👑": 4,
        "🃏": 10
        }
    SCATTER_SYMBOL = "⭐"
    SCATTER_PAYOUT = 150
    PAYLINES = [   
        ((0,0), (1,0), (2,0), (3,0), (4,0)),
        ((0,1), (1,1), (2,1), (3,1), (4,1)),
        ((0,2), (1,2), (2,2), (3,2), (4,2)),
        ((0,0), (1,1), (2,2), (3,1), (4,0)),
        ((0,2), (1,1), (2,0), (3,1), (4,2)),
        ((0,0), (1,0), (2,1), (3,2), (4,2)),
        ((0,2), (1,2), (2,1), (3,0), (4,0)),
        ((0,1), (1,2), (2,2), (3,2), (4,1)),
        ((0,1), (1,0), (2,0), (3,0), (4,1)),
        ((0,0), (1,1), (2,1), (3,1), (4,0)),
        ((0,2), (1,1), (2,1), (3,1), (4,2)),
        ((0,1), (1,2), (2,1), (3,0), (4,1)),
        ((0,1), (1,0), (2,1), (3,2), (4,1)),
        ((0,0), (1,1), (2,0), (3,1), (4,0)),
        ((0,2), (1,1), (2,2), (3,1), (4,2)),
        ((0,1), (1,1), (2,2), (3,1), (4,1)),
        ((0,1), (1,1), (2,0), (3,1), (4,1)),
        ((0,0), (1,2), (2,0), (3,2), (4,0)),
        ((0,2), (1,0), (2,2), (3,0), (4,2)),
        ((0,1), (1,0), (2,2), (3,0), (4,1))
        ]


    def __init__(self, rng: random.Random | None = None):
        self.rng = rng or random.Random()


    def _check_matches(self, symbols, target):
        matches = 0

        for s in symbols:
            if s == target or s == "🃏":
                matches += 1
            else:
                break
        return matches


    def _check_lines(self, screen):
        winnings = 0
        wins = []
        for index, payline in enumerate(self.PAYLINES):

            symbols = [screen[reel][row] for reel, row in payline]
            matches, target, payout = self._score_line(symbols)
            if matches >= 3:
                    winnings += payout      
                    win = {
                        "line": index,
                        "cells": payline[:matches],
                        "symbol": target,
                        "payout": payout
                    }
                    wins.append(win) 


        return (wins, winnings)

    def _check_scatters(self, screen):
        # Flatten the 5x3 screen into one list of 15 items
        flat_screen = [symbol for col in screen for symbol in col]
        count = flat_screen.count(self.SCATTER_SYMBOL)
        
        if count >= 3:
            return self.SCATTER_PAYOUT
        return 0


    def spin(self):
            
            screen = []
            all_symbols = list(self.symbols_multiplier.keys())

            normal_weights = [10, 9, 8, 8, 6, 5, 1]
            scatter_choices = all_symbols + [self.SCATTER_SYMBOL]
            scatter_weights = normal_weights + [3]
                

            for col in range(5):
                reel = []
                is_scatter_reel = col in [0, 2, 4]
                
                for i in range(3):
                    if is_scatter_reel and self.SCATTER_SYMBOL not in reel:
                        reel.append(self.rng.choices(scatter_choices, weights=scatter_weights, k=1)[0])
                    else:
                        reel.append(self.rng.choices(all_symbols, weights=normal_weights, k=1)[0])

                screen.append(reel)

            wins, winnings = self._check_lines(screen)
            winnings += self._check_scatters(screen)

            return SpinResult(screen=screen, winnings=winnings, wins=wins)


    def _score_line(self, symbols):
        payout = 0
        target = next((s for s in symbols if s != "🃏"), "🃏")

        matches = self._check_matches(symbols, target)
        
        if matches >= 3:    
            payout = self.lines_payouts.get(matches, 0) * self.symbols_multiplier.get(target, 0)
        
        return (matches, target, payout)
