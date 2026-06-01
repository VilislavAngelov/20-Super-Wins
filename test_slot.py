import pytest
from slot_20_super_wins import check_lines
from hypothesis import given, strategies as st

allowed_symbols = ["🍒", "🍊", "🍉", "🍇", "👑", "🃏"]

# generate a random line with 5 of the allowed symbols
line_strategy = st.lists(st.sampled_from(allowed_symbols), min_size=5, max_size=5)
# put 20 of those random lines on the screen
twenty_lines_strategy = st.lists(line_strategy, min_size=20, max_size=20)

@given(random_lines=twenty_lines_strategy)
def test_payout_boundaries(random_lines):
    starting_balance = 1000
    
    winnings = check_lines(random_lines)
    actual_balance = starting_balance + winnings
    
    # the function should always retun an integer
    assert isinstance(actual_balance, int)
    # the player cannot lose money during the payout so the balance must be at least what we started with.
    assert actual_balance >= starting_balance
    # the biggest win you can get is 20 lines of 5 jokers each and the maximum payout is $100000, so if we beat that in a single spin, something's not working 
    assert actual_balance <= starting_balance + 100000

@pytest.mark.parametrize("lines, balance, expected_balance", [
        # 5 OF A KIND (Pays 100 * multiplier)
        ( [["🍒", "🍒", "🍒", "🍒", "🍒"]], 1000, 1100 ),
        ( [["🍊", "🍊", "🍊", "🍊", "🍊"]], 1000, 1200 ),
        ( [["🍉", "🍉", "🍉", "🍉", "🍉"]], 1000, 1500 ),
        ( [["🍇", "🍇", "🍇", "🍇", "🍇"]], 1000, 2000 ),
        ( [["👑", "👑", "👑", "👑", "👑"]], 1000, 3000 ),
        ( [["🃏", "🃏", "🃏", "🃏", "🃏"]], 1000, 6000 ),

        # 4 OF A KIND (Pays 30 * multiplier)
        ( [["🍒", "🍒", "🍒", "🍒", "🍊"]], 1000, 1030 ),
        ( [["🍊", "🍊", "🍊", "🍊", "🍉"]], 1000, 1060 ),
        ( [["🍉", "🍉", "🍉", "🍉", "🍇"]], 1000, 1150 ),
        ( [["🍇", "🍇", "🍇", "🍇", "👑"]], 1000, 1300 ),
        ( [["👑", "👑", "👑", "👑", "🃏"]], 1000, 3000 ), # Becomes 5-of-a-kind (Crowns)
        ( [["🃏", "🃏", "🃏", "🃏", "🍉"]], 1000, 1500 ), # Becomes 4-of-a-kind (Watermelons)

        # 3 OF A KIND (Pays 10 * multiplier)
        ( [["🍒", "🍒", "🍒", "🍊", "🍉"]], 1000, 1010 ),
        ( [["🍊", "🍊", "🍊", "🍉", "🍇"]], 1000, 1020 ),
        ( [["🍉", "🍉", "🍉", "🍇", "👑"]], 1000, 1050 ),
        ( [["🍇", "🍇", "🍇", "👑", "🃏"]], 1000, 1100 ),
        ( [["👑", "👑", "👑", "🃏", "🍒"]], 1000, 1600 ),
        ( [["🃏", "🃏", "🃏", "🍒", "🍊"]], 1000, 1030 ),

        # 2 OF A KIND + WILD (These now pay 3-of-a-kind)
        ( [["🍒", "🍒", "🍊", "🍉", "🍇"]], 1000, 1000 ),
        ( [["🍊", "🍊", "🍉", "🍇", "👑"]], 1000, 1000 ),
        ( [["🍉", "🍉", "🍇", "👑", "🃏"]], 1000, 1000 ),
        ( [["🍇", "🍇", "👑", "🃏", "🍒"]], 1000, 1000 ),
        ( [["👑", "👑", "🃏", "🍒", "🍊"]], 1000, 1200 ),
        ( [["🃏", "🃏", "🍒", "🍊", "🍉"]], 1000, 1010 ),

        # Losing lines
        ( [["🍒", "🍊", "🍉", "🍇", "👑"]], 1000, 1000 ),
        ( [["🍊", "🍉", "🍇", "👑", "🃏"]], 1000, 1000 ),
        ( [["🍉", "🍇", "👑", "🃏", "🍒"]], 1000, 1000 ),
        ( [["🍇", "👑", "🃏", "🍒", "🍊"]], 1000, 1000 ),
        ( [["👑", "🃏", "🍒", "🍊", "🍉"]], 1000, 1000 ),
        ( [["🃏", "🍒", "🍊", "🍉", "🍇"]], 1000, 1000 ),

        # EDGE CASES
        ( [["🍊", "🍒", "🍒", "🍒", "🍒"]], 1000, 1000 ),
        ( [["🍉", "🍊", "🍊", "🍊", "🍊"]], 1000, 1000 ),
        ( [["🍒", "🍒", "🍊", "🍊", "🍊"]], 1000, 1000 ),
        ( [["🍒", "🍊", "🍒", "🍊", "🍒"]], 1000, 1000 )
    ])
def test_check_wins(lines, balance, expected_balance):

    winnings = check_lines(lines)
    actual_balance = balance + winnings
    assert actual_balance == expected_balance