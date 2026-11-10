from tkinter import *
from constants import *



root = Tk()
listCell = []
for row in range(BOARD_ROWS):
    for col in range(BOARD_COLS):
        cell = Button(root,text=f"{row},{col}")
        cell.grid(row=row,column=col)
        listCell.append(cell)


root.mainloop()