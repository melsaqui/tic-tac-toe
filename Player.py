from Cell import Cell
class Player:
    def __init__ (self,role,turn,game):
        self.role = role
        self.turn =turn
        self.game = game

    def isWon(self):
        if self.isWon_row_col():
            return True
        elif self.game.get_cell_by_axis(0, 0).val == self.role and self.game.get_cell_by_axis(1, 1).val == self.role and self.game.get_cell_by_axis(2, 2).val == self.role:
            return True
        elif self.game.get_cell_by_axis(0, 2).val == self.role and self.game.get_cell_by_axis(1, 1).val == self.role and self.game.get_cell_by_axis(2, 0).val == self.role:
            return True
        return False
        
        
    def isWon_row_col(self):
        for i in range(3):
            if self.game.get_cell_by_axis(i, 0).val == self.role and self.game.get_cell_by_axis(i, 1).val == self.role and self.game.get_cell_by_axis(i, 2).val == self.role:
                return True
            elif self.game.get_cell_by_axis(0, i).val == self.role and self.game.get_cell_by_axis(1, i).val == self.role and self.game.get_cell_by_axis(2, i).val == self.role:
                return True
        return False

            


  