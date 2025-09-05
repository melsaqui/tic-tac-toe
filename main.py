from tkinter import*
from Cell import Cell
#from PIL import Image,ImageTk
from Game import Game

root = Tk()

#background color
root.configure(bg='#1A1825')
root.geometry('470x470')
root.title("Tic-Tac-Toe")
root.resizable(False,False)
header_frame=Frame(root, width=450,height = 30)
game_frame = Frame(root)
heading = Label(header_frame, justify="center")
heading.place(relx=0.5,rely=0.5,anchor=CENTER)


header_frame.place(x=10,y=1)
game_frame.place(x=10, y=35)
Game(game_frame,root,heading)
root.mainloop()