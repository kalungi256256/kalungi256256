import tkinter as tk
from tkinter import Frame, Label, Button
from number_entry import IntEntry
import random

def main():
    root = tk.Tk()
    frm_main = Frame(root)
    frm_main.master.title("Dice")
    frm_main.pack(padx=3, pady=3, fill=tk.BOTH, expand=True)
    setup_main(frm_main)
    root.mainloop()

def setup_main(frm):
    global ent_sides, ent_count, lbl_roll, btn_roll
    
    lbl_sides = Label(frm, text="Enter the nuber of sides on the dice(2-10)")
    lbl_sides.grid(row=0, column=0)
    ent_sides = IntEntry(frm, width=2, lower_bound=2, upper_bound=20)
    ent_sides.grid(row=0, column=1)
    lbl_count = Label(frm, text="Enter the number of dices to roll")
    lbl_count.grid(row=1, column=0)
    ent_count = IntEntry(frm, width=2, lower_bound=1, upper_bound=10)
    ent_count.grid(row=1, column=1)
    btn_roll = Button(frm, text="Roll it up", command=roll_action)
    btn_roll.grid(row=2, column=0)
    lbl_roll = Label(frm, text="")
    lbl_roll.grid(row=3, column=0)

def roll_dice(sides, count):
    sum = 0
    roll_text = ""
    for roll in range(count):
        dic_roll = random.randint(1, sides)
        sum += dic_roll
        roll_text += f"Roll {roll+1}: {dic_roll} "
    roll_text += f"Total: {sum}"
    return roll_text

def roll_action():
    sides = ent_sides.get()
    count = ent_count.get()
    result = roll_dice(sides, count)
    lbl_roll.config(text=result)

if __name__ == "__main__":
    main()
