
from tkinter import *
#from Game import Game

#import settings
import random
import ctypes
import sys
import os
class Cell:
    cell_count = 9
    unmarked_cell=9
    all = []
    def __init__ (self,x,y,game,val=""):
        self.x = x
        self.y = y
        self.val = val
        self.game =game
    
    def create_btn_object (self,location,root):
        btn = Button(
            location,
            #bg='#042028',
            width = 15,
            height = 7,
            #image=default
        )
        self.root =root

        btn.bind('<Button-1>',self.left_click)

        self.cell_btn_object = btn
    def left_click(self,e):
        self.cell_btn_object.config(text =self.game.playing.role, state=DISABLED)
        self.game.updateTurns()
   
    def __repr__(self):
        return f"cell({self.x},{self.y})"
        