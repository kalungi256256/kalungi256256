import tkinter as tk
from tkinter import Frame, Label, Button
from number_entry import IntEntry
import random

def main():
    root=tk.Tk()
    frm_main=Frame(root)
    frm_main.master.tittle("Dice")
    frm_main.pack(padx=3,pady=3,fill=tk.BOTH,expand=True)
    setup_main(frm_main)
    frm_main.mainloop()

def setup_main(frm):
    lbl_sides=Label(frm,text="Enter the nuber of sides on the dice(2-10)")
    lbl_sides.grid(row=0,column=0)
    ent_sides= IntEntry(frm,width=2,lower_bound=2,upper_bound=20)
    ent_sides.grid(row=0,column=1)
    lbl_count=Label(frm,text="Enter the number of dices to roll")
    lbl_count.grid(row=1,column=0)
    ent_count = IntEntry(frm,width=2, lower_bound=1,upper_bound=10)
    ent_count.grid(row=1,column=1)
    btn_roll=Button(frm,text="Roll it up")
    btn_roll.grid(row=2,column=0)
    lbl_roll = Label(frm,text="")
    lbl_roll.grid(row=3,column=0)


def roll_dice(sides, count):
    sum=0
    roll_text =""
    for roll in range(count):
        dic_roll = random.randint(1,sides)
        sum+=dic_roll
        roll_text+=f"total{sum}"
        return roll_text    
def roll_action():
    sides-=ent_sides.get()
    lbl_roll.config(text="hit the button")
    btn_roll.config(command=roll_action)
if __name__=="__main__":
    main()
import tkinter as tk
from tkinter import Frame, Label, Button
from number_entry import IntEntry  # Make sure number_entry.py exists with IntEntry class
import random

def main():
    root = tk.Tk()
    root.title("Dice")  # Fixed: 'tittle' -> 'title'
    frm_main = Frame(root)
    frm_main.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
    setup_main(frm_main)
    root.mainloop()  # Changed from frm_main.mainloop()

def setup_main(frm):
    global ent_sides, ent_count, lbl_roll  # Make accessible to roll_action

    lbl_sides = Label(frm, text="Enter the number of sides on the dice (2-20):")
    lbl_sides.grid(row=0, column=0)
    ent_sides = IntEntry(frm, width=5, lower_bound=2, upper_bound=20)
    ent_sides.grid(row=0, column=1)

    lbl_count = Label(frm, text="Enter the number of dice to roll (1-10):")
    lbl_count.grid(row=1, column=0)
    ent_count = IntEntry(frm, width=5, lower_bound=1, upper_bound=10)
    ent_count.grid(row=1, column=1)

    btn_roll = Button(frm, text="Roll it up", command=roll_action)
    btn_roll.grid(row=2, column=0, columnspan=2)

    lbl_roll = Label(frm, text="", wraplength=200, justify="left")
    lbl_roll.grid(row=3, column=0, columnspan=2)

def roll_dice(sides, count):
    total = 0
    rolls = []
    for _ in range(count):
        die_roll = random.randint(1, sides)
        rolls.append(die_roll)
        total += die_roll
    return f"Rolls: {rolls}\nTotal: {total}"

def roll_action():
    try:
        sides = ent_sides.get()
        count = ent_count.get()
        result = roll_dice(sides, count)
        lbl_roll.config(text=result)
    except ValueError:
        lbl_roll.config(text="Please enter valid integers for both fields.")

if __name__ == "__main__":
    main()
