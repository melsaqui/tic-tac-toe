from Cell import Cell
from Player import Player
from Computer import Computer
from MsgBox import MsgBox
import random
import time
import tkinter

class Game:
    players =[]
    cells =[]
    def __init__ (self,frame,root,heading,size, view,auto=False):
        self.cell_count = size**2
        self.unmarked_cell= size**2
        self.end=False
        self.size=size

        self.players =[]
        self.cells =[]
        self.view=view

        self.auto=auto
        self.frame=frame
        self.root =root     
        self.heading=heading
        self.init_cells()
        self.players_setup()
    def players_setup(self):
        if not self.auto:
            self.players.append(Player("O",self))
            self.players.append(Player("X",self))
            self.playing=self.players[0]
            self.players[0].turn=True
            self.players[1].turn=False
            self.heading.configure(text="Player "+self.playing.role+"\'s turn")

        elif self.auto:
            self.players.append(Player(role="O",game=self))
            self.players.append(Computer(role="X",game=self,enemy=self.players[0]))
            rand=int(random.randint(0,1))
            self.playing =self.players[rand]
            if self.playing==self.players[0]:
                self.players[0].turn=True
                self.players[1].turn=False
                self.heading.configure(text="Your turn")

            else:
                self.players[1].turn=True
                self.players[0].turn=False
                self.players[1].move()
    def init_cells(self):
        for i in range (self.size):
            tkinter.Grid.rowconfigure(self.frame, i, weight=2)

            for j in range (self.size):
                tkinter.Grid.columnconfigure(self.frame, j, weight=1)

                c = (Cell(i,j,self))
                self.cells.append(c)
                c.create_btn_object(self.frame,self.root)

                c.cell_btn_object.grid(column = i, row = j,sticky="NSEW",padx=1, pady=1)

    def is_end(self):
        if self.players[0].isWon():
            self.heading.configure(text="Congratulations! "+self.players[0].role + " won!")
            self.end =True
            if MsgBox().trigger(self.auto,self.players[0]):
                self.players=[]
                self.cells=[]
                self.__init__(self.frame,self.root,self.heading,self.size,self.auto)
            else: self.view.reset()
        elif self.players[1].isWon():
            self.heading.configure(text="Congratulations! "+self.players[1].role + " won!")
            self.end =True
            if MsgBox().trigger(self.auto,self.players[1]):              
                self.reset()
            else:
                self.view.reset()

        elif self.unmarked_cell ==0 : 
            self.heading.configure(text="It's a Draw! Better Luck next time")
            self.end =True
            if MsgBox().trigger(self.auto):
                self.reset()
            else:
                self.view.reset()
        else: return  self.end 
    def reset(self):
        self.end=False
        del self.players
        del self.cells
        self.players =[]
        self.cells =[]
        self.init_cells()
        self.players_setup()
    def updateTurns(self,last_move):
        if self.players[0].turn==True:
            self.players[1].turn = True
            if not self.auto:
                self.heading.configure(text="Player "+self.players[1].role+"\'s turn")
            self.players[0].turn=False
            self.playing=self.players[1]
        else:
            self.players[0].turn=True
            if not self.auto:
                self.heading.configure(text="Player "+self.players[1].role+"\'s turn")
            self.heading.configure(text="Player "+self.players[0].role+"\'s turn")

            self.players[1].turn=False
            self.playing=self.players[0]
        if self.auto:
            if self.playing.__class__.__name__ =="Computer":
                last_arr=[last_move.x,last_move.y]
                self.playing.move(last_arr)
            else:
                self.heading.configure(text="Your Turn!")

    def get_cell_by_axis(self, x, y):
         for cell in self.cells:
             if cell.x == x and cell.y == y:
                 return cell
    
    