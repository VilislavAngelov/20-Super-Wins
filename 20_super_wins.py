from tkinter import *
from tkinter import ttk
import random


def print_screen(screen):

    on_screen = f"""{screen[0][0]} {screen[1][0]} {screen[2][0]} {screen[3][0]} {screen[4][0]}
{screen[0][1]} {screen[1][1]} {screen[2][1]} {screen[3][1]} {screen[4][1]}
{screen[0][2]} {screen[1][2]} {screen[2][2]} {screen[3][2]} {screen[4][2]}"""

    print(on_screen)

def spin(balance):
        symbols = ["🍒", "🍊", "🍉", "🍇", "👑", "🃏"]
        reel = []
        screen = []
        
        for col in range(5):
            for i in range(3):
                reel.append(random.choice(symbols))
            screen.append(reel)
            reel = []

        

        if reel == ["🍒", "🍒","🍒"]:
            print_screen(screen)
            print("You Win 30")
            balance += 30
            print(f"Balance ${balance}")
            return balance
        elif reel == ["🍊", "🍊","🍊"]:
            print_screen(screen)
            print("You Win 40")
            balance += 40
            print(f"Balance ${balance}")
            return balance
        elif reel == ["🍉", "🍉","🍉"]:
            print_screen(screen)
            print("You Win 80")
            balance += 80
            print(f"Balance ${balance}")
            return balance
        elif reel == ["🍇", "🍇","🍇"]:
            print_screen(screen)
            print("You Win 160")
            balance += 160
            print(f"Balance ${balance}")
            return balance
        elif reel == ["👑", "👑","👑"]:
            print_screen(screen)
            print("You Win 320")
            balance += 320
            print(f"Balance ${balance}")
            return balance
        elif reel == ["🃏", "🃏","🃏"]:
            print_screen(screen)
            print("You Win 1000")
            balance += 1000
            print(f"Balance ${balance}")
            return balance
        else: 
            print_screen(screen)
            print()
            print(f"Balance ${balance}")
            return balance
        #how to make the algorithm
        #how RNG works
 


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