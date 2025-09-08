class Player:
    def __init__ (self,role,game):
        self.role = role
        self.game = game

    def isWon(self):
        if self.isWon_row()==True or self.isWon_col()==True or self.isWon_diag()==True:
            return True    
        return False   
    def isWon_row(self):
        for i in range(self.game.size):
            counter=0
            for j in range(self.game.size):
                if self.game.get_cell_by_axis(i, j).val == self.role:
                    counter+=1
            if counter==self.game.size:
                return True                
        return False
    
    def isWon_col(self):
        for i in range(self.game.size):
            counter=0
            for j in range(self.game.size):
                if self.game.get_cell_by_axis(j, i).val == self.role:
                    counter+=1
            if counter==self.game.size:
                return True
        return False
    
    def isWon_diag(self):
        counter1 =0
        counter2=0
        for i in range(self.game.size):
            if self.game.get_cell_by_axis(i, i).val == self.role:
                counter1+=1
            if self.game.get_cell_by_axis(self.game.size-1-i,i).val == self.role:
                counter2+=1                      
        if counter1 == self.game.size or counter2 == self.game.size:
            return True
        return False

            


  