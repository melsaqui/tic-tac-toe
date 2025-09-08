from Cell import Cell
from Player import Player
from Computer import Computer
from MsgBox import MsgBox

class Game:
    
    def __init__ (self,frame,root,heading,size, auto=False):
        self.cell_count = size**2
        self.unmarked_cell= size**2
        self.end=False
        self.size=size
        self.players =[]
        self.cells =[]
  
        self.all = []
        self.auto=auto
        self.players.append(Player("O",True,self))
        if not auto:
            self.players.append(Player("X",False,self))
        elif auto:
            self.players.append(Computer("X",False,self,self.players[0]))

        self.frame=frame
        self.root =root
        
        self.init_cells()
        self.playing =self.players[0]
        self.heading=heading
        self.heading.configure(text="Player "+self.players[0].role+"\'s turn")
    def init_cells(self):
        for i in range (self.size):
            for j in range (self.size):
                c = (Cell(i,j,self))
                self.cells.append(c)
                c.create_btn_object(self.frame,self.root)
                c.cell_btn_object.grid(column = i, row = j)
    def is_end(self):
        if self.players[0].isWon():
            self.heading.configure(text="Congratulations! "+self.players[0].role + " won!")
            self.end =True
            if MsgBox().trigger(self.players[0]):
                Game(self.frame,self.root,self.heading,self.size,self.auto)
        elif self.players[1].isWon():
            self.heading.configure(text="Congratulations! "+self.players[1].role + " won!")
            self.end =True
            if MsgBox().trigger(self.players[1]):
                Game(self.frame,self.root,self.heading,self.size,self.auto)

        elif self.unmarked_cell ==0 : 
            self.heading.configure(text="It's a Draw! Better Luck next time")
            self.end =True
            if MsgBox().trigger():
                Game(self.frame,self.root,self.heading,self.size,self.auto)

        else: return  self.end 

    def updateTurns(self):
        if self.players[0].turn==True:
            self.players[1].turn = True
            self.heading.configure(text="Player "+self.players[1].role+"\'s turn")
            self.players[0].turn=False
            self.playing=self.players[1]
        else:
            self.players[0].turn=True
            self.heading.configure(text="Player "+self.players[0].role+"\'s turn")

            self.players[1].turn=False
            self.playing=self.players[0]
            
        if self.playing.__class__.__name__ =="Computer":
            self.playing.move()

    def get_cell_by_axis(self, x, y):
         for cell in self.cells:
             if cell.x == x and cell.y == y:
                 return cell
    
    