from tkinter import *
from tkinter import ttk
import random

root = Tk()
root.title("Slot Machine")

mainframe = ttk.Frame(root, padding=20)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

ttk.Label(mainframe, text="20 SUPER WIN").grid(column=4, row=0, sticky=S)


root.mainloop()