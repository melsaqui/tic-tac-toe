class Player:
    def __init__ (self,role,game):
        self.role = role
        self.game = game
    
    def isWon(self):
        counter_diag1 =0
        counter_diag2=0
        for i in range(self.game.size):
            counter_col=0
            counter_row =0
           
            for j in range(self.game.size):
                if self.game.get_cell_by_axis(j, i).val == self.role:
                    counter_col+=1
                if self.game.get_cell_by_axis(i, j).val == self.role:
                    counter_row+=1

            if self.game.get_cell_by_axis(i, i).val == self.role:
                counter_diag1+=1
            if self.game.get_cell_by_axis(self.game.size-1-i,i).val == self.role:
                counter_diag2+=1   
              
            if counter_col==self.game.size or counter_row==self.game.size or counter_diag1==self.game.size or counter_diag2==self.game.size:
                return True
        return False
   

            


  