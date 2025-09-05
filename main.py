from tkinter import*
from Cell import Cell
#from PIL import Image,ImageTk
from Game import Game

root = Tk()

#background color
root.configure(bg='#1A1825')
root.geometry('500x500')
root.title("Tic-Tac-Toe")
root.resizable(False,False)
'''top_frame=Frame(
    root, 
   # bg='black',
    width=100,
    height = 100)
top_frame.place(x=0, y=0)'''

game_frame = Frame(
    root,
    #bg= '#BE5A04',
    width =500,
    height = 500,
)


game_frame.place(x=10, y= 10)
Game(game_frame,root)
root.mainloop()