
from Player import Player
from functools import lru_cache
from threading import Thread
from threading import Event
from threading import Lock

import copy
import time

class Computer(Player):
    def __init__(self,role,game,enemy):
        super().__init__(role,game)
        self.enemy=enemy
        self.board_rep=[]

    def get_possible_moves(self,board):
        possible_moves=[]
        
        #center
        size=self.game.size

        for i in range(size):
            for j in range(size):
                #cell=self.board_rep
                if board[j][i]!="_" :
                    for x in range(-2,3):
                        for y in range(-2,3):
                            ref_x=i+x
                            ref_y=j+y
                            if size>ref_x>=0 and size>ref_y>=0:
                                ref_coord=[ref_x,ref_y]
                                ref_cell=board[ref_y][ref_x]
                                if  ref_cell=="_" and ref_coord not in possible_moves:
                                    possible_moves.append([ref_x,ref_y])
        possible_moves.sort(
            key=lambda move: self.move_score_to_sort(move),
            reverse=True
        )
        
        return possible_moves
    def move_score_to_sort(self,cell):
        x=cell[0]
        y=cell[1]
        score=0
        size=self.game.size
        dis_cen =abs(x-int(size/2)) + abs(y-int(size/2))
        score-=dis_cen

        if (x, y) in [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]:
            score += 3      
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy 
                if 0 <= nx < size and 0 <= ny < size:
                    if self.board_rep[ny][nx]!= self.enemy.role:
                        score+=5
                    if self.board_rep[ny][nx]!= self.role:
                        score+=4
                    
        return score
    
    def evaluate(self,board,role,enemy):
        counter_diag1 =0
        counter_diag2=0
        stop_count_diag1=False
        stop_count_diag2=False
        higher_row=float("-inf")
        higher_col=float("-inf")

        for i in range(self.game.size):
            counter_col=0
            counter_row =0
            stop_count_col=False
            stop_count_row=False

            for j in range(self.game.size):
                if board[i][j] == role and not stop_count_row:
                    counter_row+=1
                elif board[i][j] == enemy:
                    counter_row=float("-inf")
                    stop_count_row=True

                if board[j][i] == role and not stop_count_col:
                    counter_col+=1
                elif board[j][i] == enemy:
                    counter_col =float("-inf")
                    stop_count_col=True
                if stop_count_col and stop_count_row:
                    break
            if board[i][i]== role and not stop_count_diag1:
                counter_diag1+=1
            elif board[i][i] == enemy:
                stop_count_diag1 =True
                counter_diag1 =float("-inf")

            if  board[i][self.game.size-1-i] == role and not stop_count_diag2:
                counter_diag2+=1     
            elif board[i][self.game.size-1-i] == enemy:
                stop_count_diag2 =True
                counter_diag2 =float("-inf")

            if counter_row>higher_row:
                higher_row=counter_row
            if  counter_col>higher_col:
                higher_col=counter_col
      
        score = max(higher_col,higher_row,counter_diag2,counter_diag1)
        if score == self.game.size:
            return self.game.size*10000
        if score == self.game.size-1:
            return score*5000
        if score >= int(self.game.size/2) +1:
            return score*300
        elif score!=float("-inf"):
            return score*10
        return score
            
    hash_table={}
    
    #@lru_cache(maxsize=None)
    def minimax(self,board,depth,alpha,beta,isMax,max_depth):
        key = (tuple(map(tuple, board)),depth,isMax)
        if key in self.hash_table:
            return self.hash_table[key]
        
        possible_moves=self.get_possible_moves(board)
        win_score=self.game.size*10000
        one_away =(self.game.size-1)*5000
        max_score= self.evaluate(board,self.role,self.enemy.role)
        min_score= self.evaluate(board,self.enemy.role,self.role)
        actual_enemy =self.evaluate(self.board_rep,self.enemy.role,self.role)
        actual =self.evaluate(self.board_rep,self.role,self.enemy.role)

        if max_score==win_score:
            if not (min_score==one_away):
                self.stop_event.set() 
            return max_score-depth
        elif min_score==win_score:
            return depth-min_score
        elif max_score==one_away:
            return float("inf")
        elif min_score ==one_away:
           return float("-inf")        
        elif len(possible_moves) ==0 or(min_score==float("-inf") and max_score==float("-inf")):
            return 0
        elif depth==max_depth and (actual_enemy==one_away or actual==one_away) and len(possible_moves)!=0:
            print(f"max depth changed: {max_depth}")
            max_depth+=1
        elif depth==max_depth:
            if max_score>min_score:
                return max_score -depth
            elif max_score<=min_score:
                return depth-(min_score)
        if self.stop_event.is_set():
            return float("-inf"),"aborted"
        if isMax:
            best_score =float("-inf")
            if self.stop_event.is_set()==False:
                for move in possible_moves:
                    board[move[1]][move[0]]=self.role
                    score = self.minimax(board,depth + 1,alpha,beta,False,max_depth)
                    board[move[1]][move[0]]="_"
                    if isinstance(score,tuple) and score[1]=="aborted":
                        continue
                    best_score = max(score, best_score)
                    alpha= max(best_score,alpha)
                    if(beta<=alpha):
                        break
                self.hash_table[key] = best_score
            return best_score
        elif not isMax:
            best_score = float("inf")
            if self.stop_event.is_set()==False:
                for move in possible_moves:
                    board[move[1]][move[0]]=self.role
                    score = self.minimax(board,depth + 1,alpha,beta,True,max_depth)
                    board[move[1]][move[0]] = "_"
                    if isinstance(score,tuple) and score[1]=="aborted":
                        continue
                    best_score = min(score, best_score)
                    beta = min(best_score,beta)
                    if(beta<=alpha):
                        break
                self.hash_table[key] = best_score
            return best_score
        
    score_move =[]

    terminal_found=False
    results_lock = Lock()

    def get_best_move(self,move,board):
        alpha= float("-inf")
        beta= float("inf")
        if self.stop_event.is_set():
            return
        board[move[1]][move[0]] = self.role
        #score= self.minimax(board,0,alpha,beta,True,6)
        score= self.minimax(board,0,alpha,beta,True,2)
        board[move[1]][move[0]] = "_"
        with self.results_lock:
            self.score_move.append([score,move])
    
    def split_possible_move(self, possible_moves):  
        threads = []
        self.stop_event = Event()

        for move in (possible_moves):
            t = Thread(target=self.get_best_move, args=(move,copy.deepcopy(self.board_rep),))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        best_move =possible_moves[0]
        best_score=float("-inf")
        for score,move in self.score_move:
            if score!=None and best_score<score :
                best_score=score
                best_move=move
        print("Best move")
        print(best_move)
        self.score_move=[]
        self.terminal_found =False
        return best_score,best_move
    def corners(self):
        size=self.game.size
        half_size =int(size/2)
        center_cell=self.board_rep[half_size][half_size]
        corner1_cell=self.board_rep[0][0]
        corner2_cell =self.board_rep[size-1][0]
        corner3_cell =self.board_rep[0][size-1]
        corner4_cell=self.board_rep[size-1][size-1]

        if corner1_cell =="_" and corner4_cell == self.enemy:
            return 0,0
        elif corner2_cell =="_" and corner3_cell ==self.enemy:
            return 0,size-1
        elif corner3_cell =="_" and corner2_cell ==self.enemy:
            return size-1,0
        elif corner4_cell=="_" and corner1_cell ==self.enemy:
            return size-1,size-1
        elif center_cell=="_" and (corner1_cell ==self.enemy.role or corner2_cell==self.enemy.role or corner3_cell==self.enemy.role or corner4_cell ==self.enemy.role): 
            return half_size,half_size
        elif corner1_cell=="_" and center_cell ==self.enemy:
            return 0,0
        elif corner2_cell=="_" and center_cell ==self.enemy:
            return 0,size-1
        elif corner3_cell=="_" and  center_cell ==self.enemy:
            return size-1,0
        elif corner4_cell=="_" and center_cell ==self.enemy:
            return size-1,size-1
        
        elif corner1_cell=="_":
            return 0,0
        elif corner2_cell=="_":
            return 0,size-1
        elif corner3_cell=="_":
            return size-1,0
        elif corner4_cell=="_":
            return size-1,size-1
        elif center_cell=="_": 
            return half_size,half_size
        elif self.game.size%2==0: #even board so target4 cells in the corner
            for i in range(half_size-1,half_size+1):
                for j in range(half_size-1,half_size+1):
                    if self.board_rep[i][j]=="_":
                        return j,i
                    else:
                        continue
        
        elif self.game.size>3:
            for i in range(half_size-2):
                if self.board_rep[i][i]=="_":
                    return i,i
                elif self.board_rep[i][half_size-1]=="_":
                    return half_size-1,i
               
        #center

    def move_process(self,enemy_move=None):
        start_time = time.perf_counter()
        if enemy_move==None:
            self.get_board_rep()
        else:
            self.board_rep[enemy_move[1]][enemy_move[0]] = self.enemy.role
        current_enemy_score=self.evaluate(self.board_rep,self.enemy.role,self.role)

        print(f"Current enemy score: {current_enemy_score}")
        corner_move =self.corners()
        if corner_move!=None and (current_enemy_score <(self.game.size-1)*5000): 
            best_move=self.game.get_cell_by_axis(corner_move[0],corner_move[1])
            self.board_rep[corner_move[1]][corner_move[0]] = self.role

            print("best move:")
            print(best_move)
        else:   
            possible_moves=self.get_possible_moves(self.board_rep)
            print("Possible moves")
            print (possible_moves)
            data=self.split_possible_move(possible_moves)
            move=data[1]
            best_move=self.game.get_cell_by_axis(move[0],move[1])
            self.board_rep[move[1]][move[0]] = self.role

        for row in self.board_rep:
            print(row)


        best_move.val = self.role
        best_move.mark_cell()
        end_time = time.perf_counter()
        duration =end_time-start_time
        best_move=""
        print(f"processing time: {int(duration//3600)}h {int(duration//60)}m {duration%60}s")
    def get_board_rep(self):
        self.board_rep=[]
        for i in range(self.game.size):
            row = []
            for j in range(self.game.size):
                cell=self.game.get_cell_by_axis(j,i)
                if cell.val=="":
                    row.append("_")
                else:
                    row.append(cell.val)   
            self.board_rep.append(row)
        return self.board_rep
    def move(self,enemy_move=None):
        func_thread = Thread(target=self.move_process,args=(enemy_move,))
        func_thread.start()
    
        status_thread = Thread(target=self.display)
        status_thread.start()
        #func_thread.join()
        #status_thread.join()
    def display(self):
        self.game.heading.configure(text="Waiting for Computer to play...")
