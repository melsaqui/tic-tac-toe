from Cell import Cell
from Player import Player

class Game:
    players =[]
    cells =[]
    cell_count = 9
    unmarked_cell=9
    all = []
    def __init__ (self,frame,root):
        self.players.append(Player("X",True,self))
        self.players.append(Player("O",False,self))
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
    def is_end(self):
        if self.players[0].isWon():
            print(self.players[0].role + " won")
            return True
        elif self.players[1].isWon():
            print(self.players[1].role + " won")
            return True
        elif self.unmarked_cell ==0 : 
            print("Its a draw")
            return True
        else: return False
        
            

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
    
    