import pytest
from slot_machine import SlotMachine
from hypothesis import given, strategies as st

machine = SlotMachine()

allowed_symbols = ["🍒", "🍊", "🍉", "🍇", "👑", "🃏"]

reel_strategy = st.lists(st.sampled_from(allowed_symbols), min_size=3, max_size=3)
screen_strategy = st.lists(reel_strategy, min_size=5, max_size=5)

@given(screen=screen_strategy)
def test_payout_boundaries(screen):
    wins, payout = machine._check_lines(screen)
    
    max_line = machine.lines_payouts[5] * machine.symbols_multiplier["🃏"]
    max_payout = max_line * len(machine.PAYLINES)
    
    assert payout >= 0
    assert payout <= max_payout

@pytest.mark.parametrize("symbols, expected_payout", [
        # 5 OF A KIND (pays 5 × symbol multiplier)
        ( ["🍒", "🍒", "🍒", "🍒", "🍒"], 5 ),
        ( ["🍊", "🍊", "🍊", "🍊", "🍊"], 10 ),
        ( ["🍉", "🍉", "🍉", "🍉", "🍉"], 10 ),
        ( ["🍇", "🍇", "🍇", "🍇", "🍇"], 15 ),
        ( ["👑", "👑", "👑", "👑", "👑"], 20 ),
        ( ["🃏", "🃏", "🃏", "🃏", "🃏"], 50 ),

        # 4 OF A KIND (pays 1 × symbol multiplier)
        ( ["🍒", "🍒", "🍒", "🍒", "🍊"], 1 ),
        ( ["🍊", "🍊", "🍊", "🍊", "🍉"], 2 ),
        ( ["🍉", "🍉", "🍉", "🍉", "🍇"], 2 ),
        ( ["🍇", "🍇", "🍇", "🍇", "👑"], 3 ),
        ( ["👑", "👑", "👑", "👑", "🃏"], 20 ), # Becomes 5-of-a-kind (Crowns)
        ( ["🃏", "🃏", "🃏", "🃏", "🍉"], 10 ), # Becomes 5-of-a-kind (Watermelons)

        # 3 OF A KIND (pays 0.5 × symbol multiplier)
        ( ["🍒", "🍒", "🍒", "🍊", "🍉"], 0.5 ),
        ( ["🍊", "🍊", "🍊", "🍉", "🍇"], 1 ),
        ( ["🍉", "🍉", "🍉", "🍇", "👑"], 1 ),
        ( ["🍇", "🍇", "🍇", "👑", "🃏"], 1.5 ),
        ( ["👑", "👑", "👑", "🃏", "🍒"], 4 ),
        ( ["🃏", "🃏", "🃏", "🍒", "🍊"], 1 ),

        # 2 OF A KIND + WILD (These now pay 3-of-a-kind)
        ( ["🍒", "🍒", "🍊", "🍉", "🍇"], 0 ),
        ( ["🍊", "🍊", "🍉", "🍇", "👑"], 0 ),
        ( ["🍉", "🍉", "🍇", "👑", "🃏"], 0 ),
        ( ["🍇", "🍇", "👑", "🃏", "🍒"], 0 ),
        ( ["👑", "👑", "🃏", "🍒", "🍊"], 2 ),
        ( ["🃏", "🃏", "🍒", "🍊", "🍉"], 0.5 ),

        # Losing lines
        ( ["🍒", "🍊", "🍉", "🍇", "👑"], 0 ),
        ( ["🍊", "🍉", "🍇", "👑", "🃏"], 0 ),
        ( ["🍉", "🍇", "👑", "🃏", "🍒"], 0 ),
        ( ["🍇", "👑", "🃏", "🍒", "🍊"], 0 ),
        ( ["👑", "🃏", "🍒", "🍊", "🍉"], 0 ),
        ( ["🃏", "🍒", "🍊", "🍉", "🍇"], 0 ),

        # EDGE CASES
        ( ["🍊", "🍒", "🍒", "🍒", "🍒"], 0 ),
        ( ["🍉", "🍊", "🍊", "🍊", "🍊"], 0 ),
        ( ["🍒", "🍒", "🍊", "🍊", "🍊"], 0 ),
        ( ["⭐", "🍊", "⭐", "🍊", "⭐"], 15 )
    ])

def test_check_wins(symbols, expected_payout):

    matches, target, payout = machine._score_line(symbols)

    scatter_payout = machine.SCATTER_PAYOUT if symbols.count("⭐") >= 3 else 0

    assert payout + scatter_payout == expected_payout


def test_rtp():
    num_spins = 100000 
    total_payout = 0

    for i in range(num_spins):

        payout = machine.spin().payout

        total_payout += payout

    rtp_estimate = (total_payout / num_spins) * 100
    print(f"\nEstimated RTP over {num_spins} spins: {rtp_estimate:.2f}%")

    assert 94.0 <= rtp_estimate <= 98.0