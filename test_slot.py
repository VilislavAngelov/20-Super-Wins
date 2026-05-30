import pytest
from slot_20_super_wins import check_lines

@pytest.mark.parametrize("lines, balance, symbols_multiplier, expected_balance", [

    
    ( [["🍒", "🍒", "🍒", "🍒", "🍒"]], 
    1000, 
    {"🍒": 1, "🍊": 2, "🍉": 5, "🍇": 10, "👑": 20, "🃏": 50},
    1100 ),

    ( [["🍒", "🍊", "🍉", "👑", "🍒"]], 
    1000, 
    {"🍒": 1, "🍊": 2, "🍉": 5, "🍇": 10, "👑": 20, "🃏": 50},
    1000 )
])

def test_check_wins(lines, balance, symbols_multiplier, expected_balance):
    actual_balance = check_lines(lines, balance, symbols_multiplier)
    assert actual_balance == expected_balance