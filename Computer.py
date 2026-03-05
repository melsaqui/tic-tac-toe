from Player import Player
from threading import Thread
from threading import Event
from threading import Lock
from multiprocessing import Pool, Manager
import copy
import Constants
import time
class Computer(Player):
    score_move = []
    results_lock = Lock()
    hash_table = {}

    def __init__(self,role,game,enemy):
        super().__init__(role,game)
        self.enemy = enemy
        self.board_rep = []

    def get_possible_moves(size,board,radius=2):
        possible_moves = []
       # size = self.game.size
        for i in range(size):
            for j in range(size):
                if board[j][i]!="_" :
                    for x in range(-radius,radius+1):
                        for y in range(-radius,radius+1):
                            ref_x=i+x
                            ref_y=j+y
                            if size>ref_x>=0 and size>ref_y>=0:
                                ref_coord=[ref_x,ref_y]
                                ref_cell=board[ref_y][ref_x]
                                if  ref_cell=="_" and ref_coord not in possible_moves:
                                    possible_moves.append([ref_x,ref_y])
        possible_moves.sort(
            key=lambda move: Computer.move_score_to_sort(move,size,board),
            reverse=True
        )
        
        return possible_moves
    
    def move_score_to_sort(cell,size,board):
        x=cell[0]
        y=cell[1]
        score=0
        
        dis_cen =abs(x-int(size/2)) + abs(y-int(size/2))
        score-=dis_cen

        if (x, y) in [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]:
            score += 3      
        for dx in range(-3,4):
            for dy in range(-3,4):
                nx, ny = x + dx, y + dy 
                if 0 <= nx < size and 0 <= ny < size:
                    if board[ny][nx]!= "_":
                        score+=5  
        return score
    
    def evaluate(board,role,enemy,game_size):  
        higher_score =0
        win_count = game_size
            
        for i in range(game_size):
            for j in range(game_size - win_count + 1):
                window = board[i][j : j + win_count]
                if enemy not in window: 
                    higher_score = max(higher_score, window.count(role))

        for j in range(game_size):
            for i in range(game_size - win_count + 1):
                window = [board[i + x][j] for x in range(win_count)]
                if enemy not in window:
                    higher_score = max(higher_score, window.count(role))

        for i in range(game_size- win_count + 1):
            for j in range(game_size - win_count + 1):
                window = [board[i + x][j + x] for x in range(win_count)]
                if enemy not in window:
                    higher_score = max(higher_score, window.count(role))
      
        if higher_score >= win_count:
            return (higher_score/win_count)*Constants.WIN_SCORE_FACTOR
        elif higher_score == win_count-1:
            return (higher_score/win_count)*Constants.ONE_AWAY_SCORE_FACTOR
        elif higher_score >= int(win_count/2) +1:
            return (higher_score/win_count)*Constants.HALF_WAY_SCORE_FACTOR
        elif higher_score!=0:
            return higher_score*Constants.STANDARD_FACTOR
        return higher_score
                
    def minimax(board,depth,alpha,beta,isMax,max_depth,stop_event):
        global hash_table
        global game_size
        global current_score
        global role
        global enemy
        global enemy_score
        key = (tuple(map(tuple, board)),max_depth-depth,isMax)
        if key in hash_table:
            return hash_table[key]
        win_score=Constants.WIN_SCORE_FACTOR
        #one_away =(self.game.size-1)*5000
        if current_score <((game_size-1)/game_size)*Constants.ONE_AWAY_SCORE_FACTOR or enemy_score <((game_size-1)/game_size)*Constants.ONE_AWAY_SCORE_FACTOR :
           radius=1
        else:
           radius=2
        possible_moves=Computer.get_possible_moves(game_size,board,radius)
        max_score= Computer.evaluate(board,role,enemy,game_size)
        min_score= Computer.evaluate(board,enemy,role,game_size)

        if max_score>=win_score: 
            return win_score-depth
          
        elif min_score>=win_score:
            return depth-win_score
      
        elif len(possible_moves) ==0:
            return 0
        
        elif depth>=max_depth:
            return max_score-(min_score*1.5) - depth
        if stop_event.is_set():
            return -1; 
           
        if isMax:
            best_score =float("-inf")
            for move in possible_moves:
                board[move[1]][move[0]]=role
                score = Computer.minimax(board,depth + 1,alpha,beta,False,max_depth,stop_event)
                board[move[1]][move[0]]="_"
                if isinstance(score,tuple) and score[1]=="aborted":
                    return None, "aborted"
                best_score = max(score, best_score)
                alpha= max(best_score,alpha)
                if(beta<=alpha):
                    break
            hash_table[key] = best_score
            return best_score
        
        elif not isMax:
            best_score = float("inf")
            for move in possible_moves:
                board[move[1]][move[0]]=enemy
                score = Computer.minimax(board,depth + 1,alpha,beta,True,max_depth,stop_event)
                board[move[1]][move[0]] = "_"
                if isinstance(score,tuple) and score[1]=="aborted":
                    return None, "aborted"
                best_score = min(score, best_score)
                beta = min(best_score,beta)
                if(beta<=alpha):
                    break
            hash_table[key] = best_score
            return best_score
    @staticmethod
    def get_best_move(move,board):
        global stop_event
        alpha= float("-inf")
        beta= float("inf")
        if stop_event.is_set():
            return
        board[move[1]][move[0]] = role
        score= Computer.minimax(board,0,alpha,beta,True,2,stop_event)
        board[move[1]][move[0]] = "_"
        return score,move

    def split_possible_move(self, possible_moves):  
        best_score= float("-inf")
        with Manager() as manager:
            stop_event =manager.Event()
            board=copy.deepcopy(self.board_rep)
            size= self.game.size
            with Pool(initializer=init_share_worker, initargs=(stop_event,self.hash_table,self.role,self.enemy.role,size,self.current_score,self.current_enemy_score)) as pool:
                args =[(move,board) for move in possible_moves]
                results = pool.starmap(Computer.get_best_move, args)
        #pool.close()
        #pool.join()

        best_move =possible_moves[0]
        best_score=float("-inf")
        for score,move in results:
            if score!=None and best_score<score :
                best_score=score
                best_move=move
        return best_score,best_move
    
    def corners(self):
        size=self.game.size
        half_size =int(size/2)
        center_cell=self.board_rep[half_size][half_size]
        corner1_cell=self.board_rep[0][0]
        corner2_cell =self.board_rep[size-1][0]
        corner3_cell =self.board_rep[0][size-1]
        corner4_cell=self.board_rep[size-1][size-1]
        if self.game.size%2==0: #even board so target4 cells in the corner
            for i in range(half_size-1,half_size+1):
                for j in range(half_size-1,half_size+1):
                    if self.board_rep[i][j]=="_":
                        return j,i
        elif center_cell=="_": 
            return half_size,half_size
        elif corner1_cell =="_" and corner4_cell == self.enemy:
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
       
        
               
    def move_process(self,enemy_move=""):
        start_time = time.perf_counter()
        if enemy_move=="":
            self.get_board_rep()
        else:
            print(enemy_move)
            if self.board_rep==[]:
                self.get_board_rep()
            self.board_rep[enemy_move[1]][enemy_move[0]] = self.enemy.role
        game_size =self.game.size
        self.current_enemy_score=Computer.evaluate(self.board_rep,self.enemy.role,self.role,self.game.size)
        self.current_score =Computer.evaluate(self.board_rep,self.role,self.enemy.role,self.game.size)
        corner_move =self.corners()
        if (corner_move!=None) and (self.current_enemy_score <((game_size-1)/game_size)*Constants.ONE_AWAY_SCORE_FACTOR ): 
            best_move=self.game.get_cell_by_axis(corner_move[0],corner_move[1])
            self.board_rep[corner_move[1]][corner_move[0]] = self.role
        else:   
            if self.current_score <((game_size-1)/game_size)*Constants.ONE_AWAY_SCORE_FACTOR  or self.current_enemy_score <((game_size-1)/game_size)*Constants.ONE_AWAY_SCORE_FACTOR :
                radius=1
            else:
                radius=2
            possible_moves=Computer.get_possible_moves(self.game.size,self.board_rep,radius)
            data=self.split_possible_move(possible_moves)
            move=data[1]
            best_move=self.game.get_cell_by_axis(move[0],move[1])
            self.board_rep[move[1]][move[0]] = self.role
        #console representation
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
    
    def move(self,enemy_move=""):
        func_thread = Thread(target=self.move_process,args=(enemy_move,))
        func_thread.start()
    
        status_thread = Thread(target=self.display)
        status_thread.start()
    def display(self):
        self.game.heading.configure(text="Waiting for Computer to play...")
def init_share_worker(shared_event, hashed, input_role, input_enemy,size,curr_score,curr_enemy_score):
    global stop_event
    global enemy
    global role
    global hash_table
    global game_size
    global current_score
    global enemy_score
    stop_event = shared_event
    hash_table = hashed
    enemy = input_enemy
    role = input_role
    game_size= size
    current_score= curr_score
    enemy_score = curr_enemy_score