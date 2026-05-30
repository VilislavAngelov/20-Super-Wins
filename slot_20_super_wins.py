from tkinter import *
from tkinter import ttk
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

#if you hit 4 of a kind the game alo pays for the 3 in a kind within this line. This needs to be fixed

def check_lines(lines, balance):
    winnings = 0
    for line in lines:
        if line[0] == line[1] == line[2] == line[3] == line[4]:
            multiplier = symbols_multiplier.get(line[0])
            winnings += 100 * multiplier
            continue
        elif line[0] == line[1] == line[2] == line[3]:
            multiplier = symbols_multiplier.get(line[0])
            winnings += 30 * multiplier
            continue
        elif line[0] == line[1] == line[2]:
            multiplier = symbols_multiplier.get(line[0])
            winnings += 10 * multiplier
            continue
        else:
            pass

    balance += winnings        
    if winnings != 0: 
        print(f"You Win ${winnings}")

    print()
    print(f"Balance ${balance}")
    return balance   

def spin(balance):
        
        reel = []
        screen = []

        for col in range(5):
            for i in range(3):
                reel.append(random.choices(list(symbols_multiplier.keys()), weights = [10, 8, 6, 4, 2, 1], k = 1)[0])
            screen.append(reel)
            reel = []

        """{screen[0][0]} {screen[1][0]} {screen[2][0]} {screen[3][0]} {screen[4][0]}
            {screen[0][1]} {screen[1][1]} {screen[2][1]} {screen[3][1]} {screen[4][1]}
            {screen[0][2]} {screen[1][2]} {screen[2][2]} {screen[3][2]} {screen[4][2]}"""


        line1 = [screen[0][0], screen[1][0], screen[2][0], screen[3][0], screen[4][0]]
        line2 = [screen[0][1], screen[1][1], screen[2][1], screen[3][1], screen[4][1]]
        line3 = [screen[0][2], screen[1][2], screen[2][2], screen[3][2], screen[4][2]]
        line4 = [screen[0][0], screen[1][1], screen[2][2], screen[3][1], screen[4][0]]
        line5 = [screen[0][2], screen[1][1], screen[2][0], screen[3][1], screen[4][2]]
        line6 = [screen[0][0], screen[1][0], screen[2][1], screen[3][2], screen[4][2]]
        line7 = [screen[0][2], screen[1][2], screen[2][1], screen[3][0], screen[4][0]]
        line8 = [screen[0][1], screen[1][2], screen[2][2], screen[3][2], screen[4][1]]
        line9 = [screen[0][1], screen[1][0], screen[2][0], screen[3][0], screen[4][1]]
        line10 = [screen[0][0], screen[1][1], screen[2][1], screen[3][1], screen[4][0]]
        line11 = [screen[0][2], screen[1][1], screen[2][1], screen[3][1], screen[4][2]]
        line12 = [screen[0][1], screen[1][2], screen[2][1], screen[3][0], screen[4][1]]
        line13 = [screen[0][1], screen[1][0], screen[2][1], screen[3][2], screen[4][1]]
        line14 = [screen[0][0], screen[1][1], screen[2][0], screen[3][1], screen[4][0]]
        line15 = [screen[0][2], screen[1][1], screen[2][2], screen[3][1], screen[4][2]]
        line16 = [screen[0][1], screen[1][1], screen[2][2], screen[3][1], screen[4][1]]
        line17 = [screen[0][1], screen[1][1], screen[2][0], screen[3][1], screen[4][1]]
        line18 = [screen[0][0], screen[1][2], screen[2][0], screen[3][2], screen[4][0]]
        line19 = [screen[0][2], screen[1][0], screen[2][2], screen[3][0], screen[4][2]]
        line20 = [screen[0][1], screen[1][0], screen[2][2], screen[3][0], screen[4][1]]

        lines = []

        lines.append(line1)
        lines.append(line2)
        lines.append(line3)
        lines.append(line4)
        lines.append(line5)
        lines.append(line6)
        lines.append(line7)
        lines.append(line8)
        lines.append(line9)
        lines.append(line10)
        lines.append(line11)
        lines.append(line12)
        lines.append(line13)
        lines.append(line14)
        lines.append(line15)
        lines.append(line16)
        lines.append(line17)
        lines.append(line18)
        lines.append(line19)
        lines.append(line20)

        print_screen(screen)

        return check_lines(lines, balance)


        

"""
        if line1[0] == line1[1] == line1[2] and line1[0] == "🍒":
            print("You Win 30")
            balance += 30
            print(f"Balance ${balance}")
            return balance
        elif line1[0] == line1[1] == line1[2] and line1[0] == "🍊":
            print("You Win 40")
            balance += 40
            print(f"Balance ${balance}")
            return balance
        elif line1[0] == line1[1] == line1[2] and line1[0] == "🍉":
            print("You Win 80")
            balance += 80
            print(f"Balance ${balance}")
            return balance
        elif line1[0] == line1[1] == line1[2] and line1[0] == "🍇":
            print("You Win 160")
            balance += 160
            print(f"Balance ${balance}")
            return balance
        elif line1[0] == line1[1] == line1[2] and line1[0] == "👑":
            print("You Win 320")
            balance += 320
            print(f"Balance ${balance}")
            return balance
        elif line1[0] == line1[1] == line1[2] and line1[0] == "🃏":
            print("You Win 1000")
            balance += 1000
            print(f"Balance ${balance}")
            return balance
        else:
            print()
            print(f"Balance ${balance}")
            return balance

        #how to make the algorithm
        #how RNG works
 """


def main():
 
    balance = 1000
    bet = 10

    print("##########################")
    print("##### 20 SUPER WINS ######")
    print("['🃏', '🃏', '🃏']")
    print("##### Place Your Bet #####")
    print(f"### Balance ${balance} ###")
    while balance > bet:

        balance -= bet
        input("")
        balance = spin(balance) 


    
if __name__ == "__main__":
    main()
    print("Insufficient Balance")



'''
root = Tk()
root.title("Slot Machine")

mainframe = ttk.Frame(root, padding=20)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

ttk.Label(mainframe, text="20 SUPER WIN").grid(column=4, row=0, sticky=S)



root.mainloop()
'''

'''
TASK LIST
1. Break down the task to smaller tasks
    -How a slot machine works
    -How to display the reels
    -Check if you have enough money to spin
    -How to deduct spin from balance
    -How to add wins to balance
    -How to define the symbols
    -How to make the slot algorithm
    -How to display balance
    -How to calculate wins
    -Do I have to use OOP for a slot machine
    -How to make the columns show the symbols one by one on the slot left to right
    -How do I mmake the 20 SUPER WINS a title 
    -How to define the lines
    -How do I change the bet
    -How do I spin by clicking spacebar
    -How to position the widgets the way I want 
    -How to make a symbol wild
    -Calculate the RTP (Aim between 95 and 98 percent)
but since it's not assigned to any variable,
it is effectively ignored during execution.
'''