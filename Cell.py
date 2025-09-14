
from tkinter import *
class Cell:
    def __init__ (self,x,y,game,val=""):
        self.x = x
        self.y = y
        self.val = val
        self.game =game
    
    def create_btn_object (self,location,root):
        if self.game.size==5:
            width = 3
            height = 1
            font=("Arial",29,"bold")
        elif self.game.size==10:
            width = 3
            height = 1  
            font=("Arial",13,"bold")
        elif self.game.size==3:
            width = 5
            height = 2
            font=("Arial",31,"bold")
        btn = Button(
            location,
            bg='#042028',
            width = width,
            height = height,
            font=font,
        )

       
        self.root =root

        btn.bind('<Button-1>',self.left_click)

        self.cell_btn_object = btn
    def left_click(self,e):
        if self.val=="" and not self.game.end and self.game.playing.__class__.__name__ !="Computer":
            self.mark_cell()
   
            
    def mark_cell(self):
        if self.game.playing.role == "X":
            self.cell_btn_object.config(text =self.game.playing.role,fg="red")
        else:
            self.cell_btn_object.config(text =self.game.playing.role,fg="blue")
        self.val = self.game.playing.role
        self.game.unmarked_cell -=1
        
        if self.game.is_end()==False:
            self.game.updateTurns()

    def __repr__(self):
        return f"cell({self.x},{self.y})"
        