import pytest
from slot_engine import spin, check_lines, check_scatters , score_line
from hypothesis import given, strategies as st

allowed_symbols = ["🍒", "🍊", "🍉", "🍇", "👑", "🃏"]

reel_strategy = st.lists(st.sampled_from(allowed_symbols), min_size=3, max_size=3)
screen_strategy = st.lists(reel_strategy, min_size=5, max_size=5)

@given(screen=screen_strategy)
def test_payout_boundaries(screen):
    starting_balance = 1000
    
    wins, winnings = check_lines(screen)
    actual_balance = starting_balance + winnings
    
    # the function should always retun an integer
    assert isinstance(actual_balance, int)
    # the player cannot lose money during the payout so the balance must be at least what we started with.
    assert actual_balance >= starting_balance
    # the biggest win you can get is 20 lines of 5 jokers each and the maximum payout is $100000, so if we beat that in a single spin, something's not working 
    assert actual_balance <= starting_balance + 100000

@pytest.mark.parametrize("symbols, balance, expected_balance", [
        # 5 OF A KIND (Pays 100 * multiplier)
        ( ["🍒", "🍒", "🍒", "🍒", "🍒"], 1000, 1050 ),
        ( ["🍊", "🍊", "🍊", "🍊", "🍊"], 1000, 1100 ),
        ( ["🍉", "🍉", "🍉", "🍉", "🍉"], 1000, 1100 ),
        ( ["🍇", "🍇", "🍇", "🍇", "🍇"], 1000, 1150 ),
        ( ["👑", "👑", "👑", "👑", "👑"], 1000, 1200 ),
        ( ["🃏", "🃏", "🃏", "🃏", "🃏"], 1000, 1500 ),

        # 4 OF A KIND (Pays 30 * multiplier)
        ( ["🍒", "🍒", "🍒", "🍒", "🍊"], 1000, 1010 ),
        ( ["🍊", "🍊", "🍊", "🍊", "🍉"], 1000, 1020 ),
        ( ["🍉", "🍉", "🍉", "🍉", "🍇"], 1000, 1020 ),
        ( ["🍇", "🍇", "🍇", "🍇", "👑"], 1000, 1030 ),
        ( ["👑", "👑", "👑", "👑", "🃏"], 1000, 1200 ), # Becomes 5-of-a-kind (Crowns)
        ( ["🃏", "🃏", "🃏", "🃏", "🍉"], 1000, 1100 ), # Becomes 5-of-a-kind (Watermelons)

        # 3 OF A KIND (Pays 10 * multiplier)
        ( ["🍒", "🍒", "🍒", "🍊", "🍉"], 1000, 1005 ),
        ( ["🍊", "🍊", "🍊", "🍉", "🍇"], 1000, 1010 ),
        ( ["🍉", "🍉", "🍉", "🍇", "👑"], 1000, 1010 ),
        ( ["🍇", "🍇", "🍇", "👑", "🃏"], 1000, 1015 ),
        ( ["👑", "👑", "👑", "🃏", "🍒"], 1000, 1040 ),
        ( ["🃏", "🃏", "🃏", "🍒", "🍊"], 1000, 1010 ),

        # 2 OF A KIND + WILD (These now pay 3-of-a-kind)
        ( ["🍒", "🍒", "🍊", "🍉", "🍇"], 1000, 1000 ),
        ( ["🍊", "🍊", "🍉", "🍇", "👑"], 1000, 1000 ),
        ( ["🍉", "🍉", "🍇", "👑", "🃏"], 1000, 1000 ),
        ( ["🍇", "🍇", "👑", "🃏", "🍒"], 1000, 1000 ),
        ( ["👑", "👑", "🃏", "🍒", "🍊"], 1000, 1020 ),
        ( ["🃏", "🃏", "🍒", "🍊", "🍉"], 1000, 1005 ),

        # Losing lines
        ( ["🍒", "🍊", "🍉", "🍇", "👑"], 1000, 1000 ),
        ( ["🍊", "🍉", "🍇", "👑", "🃏"], 1000, 1000 ),
        ( ["🍉", "🍇", "👑", "🃏", "🍒"], 1000, 1000 ),
        ( ["🍇", "👑", "🃏", "🍒", "🍊"], 1000, 1000 ),
        ( ["👑", "🃏", "🍒", "🍊", "🍉"], 1000, 1000 ),
        ( ["🃏", "🍒", "🍊", "🍉", "🍇"], 1000, 1000 ),

        # EDGE CASES
        ( ["🍊", "🍒", "🍒", "🍒", "🍒"], 1000, 1000 ),
        ( ["🍉", "🍊", "🍊", "🍊", "🍊"], 1000, 1000 ),
        ( ["🍒", "🍒", "🍊", "🍊", "🍊"], 1000, 1000 ),
        ( ["⭐", "🍊", "⭐", "🍊", "⭐"], 1000, 1150 )
    ])

def test_check_wins(symbols, balance, expected_balance):

    print(symbols)

    matches, target, payout = score_line(symbols)

    flat_screen = [symbol for col in symbols for symbol in col]
    scatter_count = flat_screen.count("⭐")
    scatter_winnings = 150 if scatter_count >= 3 else 0
    
    actual_balance = balance + payout + scatter_winnings
    assert actual_balance == expected_balance


def test_rtp():
    num_spins = 100000 
    total_bets = 0
    total_wins = 0
    bet_size = 10

    for i in range(num_spins):

        total_bets += bet_size

        screen , winnings , wins = spin()

        total_wins += winnings

    rtp_estimate = (total_wins / total_bets) * 100
    print(f"\nEstimated RTP over {num_spins} spins: {rtp_estimate:.2f}%")

    assert 94.0 <= rtp_estimate <= 98.0