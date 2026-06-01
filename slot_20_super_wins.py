import random

symbols_multiplier = {
            "🍒": 1,
            "🍊": 2,
            "🍉": 5,
            "🍇": 10,
            "👑": 20,
            "🃏": 50
            }

def print_screen(screen):

    on_screen = f"""{screen[0][0]} {screen[1][0]} {screen[2][0]} {screen[3][0]} {screen[4][0]}
{screen[0][1]} {screen[1][1]} {screen[2][1]} {screen[3][1]} {screen[4][1]}
{screen[0][2]} {screen[1][2]} {screen[2][2]} {screen[3][2]} {screen[4][2]}"""

    print(on_screen)


def check_lines(lines):
    winnings = 0
    # if you have 5 of a kind they pay a base of 100, 4 pay 30 and 3 pay 3
    lines_payouts = {5 : 100, 4 : 30, 3 : 10}

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
  

def spin(balance):
        
        reel = []
        screen = []

        for col in range(5):
            for i in range(3):
                reel.append(random.choices(list(symbols_multiplier.keys()), weights = [10, 8, 6, 4, 2, 1], k = 1)[0])
            screen.append(reel)
            reel = []

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

        return screen, check_lines(lines)


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
        
        screen, winnings = spin(balance)
        balance += winnings  

        print_screen(screen)

        if winnings != 0: 
            print(f"You Win ${winnings}")

        print()
        print(f"Balance ${balance}") 




if __name__ == "__main__":
    main()
    print("Insufficient Balance")
