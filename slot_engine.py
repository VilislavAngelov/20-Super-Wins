import random

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

def print_screen(screen):

    on_screen = f"""{screen[0][0]} {screen[1][0]} {screen[2][0]} {screen[3][0]} {screen[4][0]}
{screen[0][1]} {screen[1][1]} {screen[2][1]} {screen[3][1]} {screen[4][1]}
{screen[0][2]} {screen[1][2]} {screen[2][2]} {screen[3][2]} {screen[4][2]}"""

    print(on_screen)

#TODO make the winnings less frequent but more in amount so the game is more fun or volatile, as the game currently is draining the balance in a more steady and consistent fashion.
def check_lines(lines):
    winnings = 0
    # if you have 5 of a kind they pay a base of 100, 4 pay 30 and 3 pay 3
    lines_payouts = {5 : 50, 4 : 10, 3 : 5}

    for line in lines:

        target = next((s for s in line if s != "🃏"), "🃏")

        matches = 0
        for s in line:
            if s == target or s == "🃏":
                matches += 1
            else:
                break

        if matches >= 3:
            winnings += lines_payouts.get(matches, 0) * symbols_multiplier.get(target, 0)       

    return winnings 

def check_scatters(screen):
    # Flatten the 5x3 screen into one list of 15 items
    flat_screen = [symbol for col in screen for symbol in col]
    count = flat_screen.count(SCATTER_SYMBOL)
    
    if count >= 3:
        return SCATTER_PAYOUT
    return 0

def spin():
        
        screen = []
        all_symbols = list(symbols_multiplier.keys())

        normal_weights = [10, 9, 8, 8, 6, 5, 1]
        scatter_choices = all_symbols + [SCATTER_SYMBOL]
        scatter_weights = normal_weights + [3]
            

        for col in range(5):
            reel = []
            is_scatter_reel = col in [0, 2, 4]
            
            for i in range(3):
                if is_scatter_reel and SCATTER_SYMBOL not in reel:
                    reel.append(random.choices(scatter_choices, weights=scatter_weights, k=1)[0])
                else:
                    reel.append(random.choices(all_symbols, weights=normal_weights, k=1)[0])

            screen.append(reel)
            

        lines = [
            [screen[0][0], screen[1][0], screen[2][0], screen[3][0], screen[4][0]],
            [screen[0][1], screen[1][1], screen[2][1], screen[3][1], screen[4][1]],
            [screen[0][2], screen[1][2], screen[2][2], screen[3][2], screen[4][2]],
            [screen[0][0], screen[1][1], screen[2][2], screen[3][1], screen[4][0]],
            [screen[0][2], screen[1][1], screen[2][0], screen[3][1], screen[4][2]],
            [screen[0][0], screen[1][0], screen[2][1], screen[3][2], screen[4][2]],
            [screen[0][2], screen[1][2], screen[2][1], screen[3][0], screen[4][0]],
            [screen[0][1], screen[1][2], screen[2][2], screen[3][2], screen[4][1]],
            [screen[0][1], screen[1][0], screen[2][0], screen[3][0], screen[4][1]],
            [screen[0][0], screen[1][1], screen[2][1], screen[3][1], screen[4][0]],
            [screen[0][2], screen[1][1], screen[2][1], screen[3][1], screen[4][2]],
            [screen[0][1], screen[1][2], screen[2][1], screen[3][0], screen[4][1]],
            [screen[0][1], screen[1][0], screen[2][1], screen[3][2], screen[4][1]],
            [screen[0][0], screen[1][1], screen[2][0], screen[3][1], screen[4][0]],
            [screen[0][2], screen[1][1], screen[2][2], screen[3][1], screen[4][2]],
            [screen[0][1], screen[1][1], screen[2][2], screen[3][1], screen[4][1]],
            [screen[0][1], screen[1][1], screen[2][0], screen[3][1], screen[4][1]],
            [screen[0][0], screen[1][2], screen[2][0], screen[3][2], screen[4][0]],
            [screen[0][2], screen[1][0], screen[2][2], screen[3][0], screen[4][2]],
            [screen[0][1], screen[1][0], screen[2][2], screen[3][0], screen[4][1]]
        ]

        outcome = {
            "screen": screen,
            "winnings": check_lines(lines) + check_scatters(screen)
        }

        return outcome


def main():
 
    balance = 1000
    bet = 10

    print("##########################")
    print("##### 20 SUPER WINS ######")
    print("['🃏', '🃏', '🃏']")
    print("##### Place Your Bet #####")
    print(f"### Balance ${balance} ###")
    while balance > bet:

        input("")
        balance -= bet
        
        result = spin()

        screen = result["screen"]
        winnings = result["winnings"]

        balance += winnings

        print_screen(screen)

        if winnings != 0: 
            print(f"You Win ${winnings}")

        print()
        print(f"Balance ${balance}") 

    print("Insufficient Balance")




if __name__ == "__main__":
    main()
    
