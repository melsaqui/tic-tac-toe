
from tkinter import *
#from Game import Game

#import settings
import ctypes
import sys
import os
class Cell:
   
    def __init__ (self,x,y,game,val=""):
        self.x = x
        self.y = y
        self.val = val
        self.game =game
    
    def create_btn_object (self,location,root):
        #big_font
        btn = Button(
            location,
            #bg='#042028',
            width = 12,
            height = 6,
            font=("Arial",16,"bold")
        )
        self.root =root

        btn.bind('<Button-1>',self.left_click)

        self.cell_btn_object = btn
    def left_click(self,e):
        if self.val=="" and not self.game.end:
            self.cell_btn_object.config(text =self.game.playing.role, state=DISABLED)
            self.val = self.game.playing.role
            self.game.unmarked_cell -=1
            if self.game.is_end()==False:
                self.game.updateTurns()
            
    def __repr__(self):
        return f"cell({self.x},{self.y})"
        