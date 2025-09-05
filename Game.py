from Cell import Cell
from Player import Player

class Game:
    players =[]
    cells =[]
    def __init__ (self,frame,root):
        self.players.append(Player("X",True))
        self.players.append(Player("O",False))
        self.frame=frame
        self.root =root
        self.init_cells()
        self.playing =self.players[0]

    def init_cells(self):
        for i in range (3):
            for j in range (3):
                c = (Cell(i,j,self))
                self.cells.append(c)
                c.create_btn_object(self.frame,self.root)
                c.cell_btn_object.grid(column = i, row = j)

    def updateTurns(self):
        if self.players[0].turn==True:
            self.players[1].turn = True
            self.players[0].turn=False
            self.playing=self.players[1]
        else:
            self.players[0].turn=True
            self.players[1].turn=False
            self.playing=self.players[0]

    def get_cell_by_axis(self, x, y):
        #return a cell object based on x, y
         for cell in self.cells:
             if cell.x == x and cell.y == y:
                 return cell
    
    