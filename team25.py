import sys
import random
import signal
import time
import copy

class Player25:
    def __init__(self):
        self.min_limit=3
        self.max_depth=3
        self.my_points=0
        self.opp_points=0
        self.flag=0
        self.end=0
        self.start_time=time.clock()
#        self.multi=[[0 for i in range(4)] for j in range(4)]
        pass


    def getMoves(self, board,block,old_move):
        #returns the valid cells allowed given the last move and the current board state
        allowed_cells = []
        allowed_block = [old_move[0]%4, old_move[1]%4]
        #checks if the move is a free move or not based on the rules

        if old_move != (-1,-1) and block[allowed_block[0]][allowed_block[1]] == '-':
            for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
                for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
                    if board[i][j] == '-':
                        allowed_cells.append((i,j))
        else:
            for i in range(16):
                for j in range(16):
                    if board[i][j] == '-' and block[i/4][j/4] == '-':
                        allowed_cells.append((i,j))
        return allowed_cells    




    def update_block(self,board,block,ply,blockNo):
        x = blockNo/4
        y = blockNo%4

        temp_block = block

        for i in range(4):
            #checking for horizontal pattern(i'th row)
            if (board[4*x+i][4*y] == board[4*x+i][4*y+1] == board[4*x+i][4*y+2] == board[4*x+i][4*y+3]) and (board[4*x+i][4*y] == ply):
                temp_block[x][y] = ply
                return temp_block
            #checking for vertical pattern(i'th column)
            if (board[4*x][4*y+i] == board[4*x+1][4*y+i] == board[4*x+2][4*y+i] == board[4*x+3][4*y+i]) and (board[4*x][4*y+i] == ply):
                temp_block[x][y] = ply
                return temp_block

        #checking for diagnol pattern
        if (board[4*x][4*y] == board[4*x+1][4*y+1] == board[4*x+2][4*y+2] == board[4*x+3][4*y+3]) and (board[4*x][4*y] == ply):
            temp_block[x][y] = ply
            return temp_block
        if (board[4*x+3][4*y] == board[4*x+2][4*y+1] == board[4*x+1][4*y+2] == board[4*x][4*y+3]) and (board[4*x+3][4*y] == ply):
            temp_block[x][y] = ply
            return temp_block

        #checking if a block has any more cells left or has it been drawn
        for i in range(4):
            for j in range(4):
                if board[4*x+i][4*y+j] =='-':
                    return temp_block
        temp_block[x][y] = 'd'
        return temp_block



    def minimax(self,board,block,ourflag,otherflag,depth,node_type,alpha,beta,max_row,max_col,prev_move):
        
        moves = self.getMoves(board,block,prev_move)
#       print len(moves)

        if depth==0:
            if len(moves)<6 and self.flag==0:
                self.max_depth=4

        if depth>=self.max_depth:
            utility = self.find_utility(board,block,ourflag,otherflag);
            return (utility,max_row,max_col)


#       moves = self.getMoves(board,block,prev_move)


#       random.shuffle(moves)

        for move in moves:
            blockNo = (move[0]/4)*4 + (move[1]/4)
            if node_type==0:
                board[move[0]][move[1]]=ourflag
            else:
                board[move[0]][move[1]]=otherflag

            fl=otherflag
            if node_type==0:
                fl=ourflag
            temp_block=self.update_block(board,block,fl,blockNo)

            if node_type==0:
                PartUtil = self.minimax(board,temp_block,ourflag,otherflag,depth+1,1,alpha,beta,max_row,max_col,move)

                utility = round(PartUtil[0],8)
                if utility > alpha:
                    alpha = utility
                    max_row = move[0]
                    max_col = move[1]

                if self.end==0:
                    if (time.clock()- self.start_time) >13:
                        self.end=1
                        break
                else:
                    break

            else:               
                PartUtil = self.minimax(board,temp_block,ourflag,otherflag,depth+1,0,alpha,beta,max_row,max_col,move)

                utility = round(PartUtil[0],8)
                if utility < beta:
                    beta = utility
                    max_row = move[0]
                    max_col = move[1]
                if self.end==0:
                    if (time.clock()- self.start_time) >13:
                        self.end=1
                        break
                else:
                    break
            
            board[move[0]][move[1]] = '-'

            if alpha >= beta:
                break

        if depth==0:
            if max_row == -1 and max_col == -1:
                max_row = moves[0][0]
                max_col = moves[0][1]


        if node_type==0:
            return (alpha,max_row,max_col)
        else:
            return (beta,max_row,max_col)



    def move(self,board,old_move,ourflag):
        self.start_time=time.clock()
        if ourflag=='o':
            otherflag='x'
        else:
            otherflag='o'

        self.my_points=board.block_status.count(ourflag)
        self.opp_points=board.block_status.count(otherflag)

        temp_board=copy.deepcopy(board.board_status)
        temp_block=copy.deepcopy(board.block_status)

        count=0
        for i in range(16):
            for j in range(16):
                if temp_board[i][j]=='-' and temp_block[i/4][j/4]=='-':
                    count+=1

        if count<=50 and count>25:
            self.max_depth=5
        elif count<=25 and count>=15:
            self.max_depth=6
        elif count<=14 and count>10:
            self.max_depth=7
        elif count<=10 and count>=5:
            self.max_depth=10
        elif count <=5:
            self.max_depth=10

#        print self.max_depth

        if self.max_depth > self.min_limit:
            self.flag=1
        
        nextStep = self.minimax(temp_board,temp_block,ourflag,otherflag,0,0,-10000000000000.0,10000000000000.0,-1,-1,old_move)
#       print "netTime", time.clock()-start_time
#        print "move", nextStep[1],nextStep[2]
#        print self.max_depth
        self.max_depth=3
        self.flag=0
        self.end=0
        return (nextStep[1],nextStep[2])

    def calc_eachUtility(self, cp, ce, cd,mult):
        temp = 0
        if cd == 0:
            if cp == 0:
                temp = -100000
            elif ce == 0:
                temp = 100000
        elif ce == 0:
            if cd == 1:
                temp = 100
            elif cd == 2:
                temp = 2
        elif cp == 0:
            if cd == 1:
                temp = -100
            elif cd == 2:
                temp = -2
        return temp

    def calc_utility(self, board,ourflag,otherflag):

        gain1 = 0
        for i in range(4):
            for j in range(4):
                if ((i == 0 or i == 3) and (j == 1 or j == 2)) or ((i == 1 or i == 2) and (j == 0 or j == 3)):
                    if board[i][j] == ourflag:
                        gain1 += 5
                    elif board[i][j] == otherflag:
                        gain1 -= 5
                else:
                    if board[i][j] == ourflag:
                        gain1 += 5
                    elif board[i][j] == otherflag:
                        gain1 -= 5

        gain2 = 0
        for i in range(4):
            ce=0
            cp=0
            cd=0
            for j in range(4):
                if board[i][j]==ourflag:
                    cp+=1
                elif board[i][j]==otherflag:
                    ce+=1
                else:
                    cd+=1

            gain2+=self.calc_eachUtility(cp,ce,cd,1)

        for i in range(4):
            ce=0
            cp=0
            cd=0
            for j in range(4):
                if board[j][i]==ourflag:
                    cp+=1
                elif board[j][i]==otherflag:
                    ce+=1
                else:
                    cd+=1

            gain2+=self.calc_eachUtility(cp,ce,cd,1)
        
        ce=0
        cp=0
        cd=0

        for i in range(4):
            if board[i][i]==ourflag:
                cp+=1
            elif board[i][i]==otherflag:
                ce+=1
            else:
                cd+=1

        gain2+=self.calc_eachUtility(cp,ce,cd,1)

        ce=0
        cp=0
        cd=0

        for i in range(4):
            if board[i][3-i]==ourflag:
                cp+=1
            elif board[i][3-i]==otherflag:
                ce+=1
            else:
                cd+=1

        gain2+=self.calc_eachUtility(cp,ce,cd,1)

        return (gain1 + (gain2 * 10))

    def find_utility(self, board,block,ourflag,otherflag):

        gain = 0
        temp_board = [[0 for i in range(4)] for j in range(4)]
        for i in range(0, 16, 4):
            for j in range(0, 16, 4):
                for p1 in range(i, i + 4):
                    for p2 in range(j, j + 4):
                        temp_board[p1 - i][p2 - j] = board[p1][p2]
                if ((i%4 == 0 or i%4 == 3) and (j%4 == 1 or j%4 == 2)) or ((i%4 == 1 or i%4 == 2) and (j%4 == 0 or j%4 == 3)):
                    mult = 1
                else:
                    mult = 1
                gain += self.calc_utility(temp_board,ourflag,otherflag) * mult


        return (gain + self.calc_utility(board,ourflag,otherflag) * 100)
