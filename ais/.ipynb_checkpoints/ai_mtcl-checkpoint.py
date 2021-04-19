from ais.ai_base import ai_base
import random
import math
import time
from common import *

       

def new_board(size):
    return [[0 for i in range(size)] for j in range(size)]
def estimate_point(chessboard, P, color):
    # have some problems recognizing 3+3 situation
    i, j = P[0], P[1]
    ldir = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
    rdir = [(1, 0), (1, 1), (0, 1), (-1, 1)]
    score = 1
    for c in range(1, 3):
        K = 1
        if c != color: K += 0.5
        count_3 = 0
        count_4 = 0
        count_5 = 0
        for d in range(4):
            count = 3
            max_len = 1
            for step in range(1, 5):
                pos = (i+ldir[d][0]*step, j+ldir[d][1]*step)
                if chessboard.isLegal(pos):
                    if chessboard[pos[0]][pos[1]] == c:
                        count += 3
                        max_len += 1
                    elif chessboard.isEmpty(pos):
                        count += 1
                        max_len += 1
                        break
                    else:
                        break
                else:
                    break

            for step in range(1, 5):
                pos = (i+rdir[d][0]*step, j+rdir[d][1]*step)
                if chessboard.isLegal(pos):
                    if chessboard[pos[0]][pos[1]] == c:
                        count += 3
                        max_len += 1
                    elif chessboard.isEmpty(pos):
                        count += 1
                        max_len += 1
                        break
                    else:
                        break
                else:
                    break
            if max_len > 4:
                if count == 11:
                    score += 10*K
                    count_3 += 1
                elif count >= 15:
                    score += 10000*K
                    count_5 += 1
                elif count in [13, 14]:
                    if count == 13:
                        score += 20*K
                    else:
                        score += 100*K
                    count_4 += 1
        if count_3 + count_4 + count_5 > 1:
            score += 1000*K
    return 3**int(math.log(score))
def quick_move(board, color, ava):
    # quick make decision
    r = []
    for p in ava:
        t = estimate_point(board, p, color)
        r += [p] * t
    return random.choice(r)
def quick_check(board, point, ava):
    # quick check win or loss
    n = len(board)
    ldir = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
    rdir = [(1, 0), (1, 1), (0, 1), (-1, 1)]
    c = board[point[0]][point[1]]
    for i in range(4):
        lc = 0
        rc = 0
        for j in range(1, 5):
            x_n = point[0]+j*ldir[i][0]
            y_n = point[1]+j*ldir[i][1]
            if 0 <= x_n and x_n < n and 0 <= y_n and y_n < n and board[x_n][y_n] == c:
                lc += 1
            else:
                break
        for j in range(1, 5):
            x_n = point[0]+j*rdir[i][0]
            y_n = point[1]+j*rdir[i][1]
            if 0 <= x_n and x_n < n and 0 <= y_n and y_n < n and board[x_n][y_n] == c:
                rc += 1
            else:
                break
        if lc+rc+1 >= 5:
            #board .show()
            return c
    if len(ava) == 0:
        return -1
    return 0
            
def calc_av(board, point, last):
    # quick calc available places on board
    ret = last.copy()
    n = len(board)
    if point == None:
        # from null chess
        for i in range(n):
            for j in range(n):
                if board[i][j] != 0:
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            i1 = i+dx
                            j1 = j+dy
                            if (dx != 0 or dy != 0) and board.isLegal((i1, j1)) and board.isEmpty((i1, j1)):
                                ret.add((i1, j1))
    else:
        # build from last with a new point
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                i1 = point[0]+dx
                j1 = point[1]+dy
                if (dx != 0 or dy != 0) and board.isLegal((i1, j1)) and board.isEmpty((i1, j1)):
                    ret.add((i1, j1))  
        ret.remove(point)

    return ret
    
def random_walk(board, color, ava):
    
    while True:
        next_pos = quick_move(board, color, ava)
        ava = calc_av(board, next_pos, ava)
        board[next_pos[0]][next_pos[1]] = color
        flag = quick_check(board, next_pos, ava)
        if flag != 0:
            return flag
        color = 3-color

class tree_node:
    def __init__(self, point, ava, K):
        self.ava = ava
        self.point = point
        self.info = [0, 0]
        self.son = None
        self.K = K
        self.flag = 0  #if the state is already win
    def addSon(self, board, color):
        if self.flag != 0:
            return None
        self.son = []
        # find possible place to move
        for pt in self.ava:
            son_node = tree_node(pt, calc_av(board, pt, self.ava), self.K)
            board[pt[0]][pt[1]] = color
            son_node.flag = quick_check(board, pt, son_node.ava)
            board[pt[0]][pt[1]] = 0
            self.son.append(son_node)
        # add all possible place
        
        return self.bestSon()
    def bestSon(self):
        best_score = -1
        best_son = None
        for son in self.son:
            score = (son.info[0]+0.1)/(son.info[1]+0.1)+self.K*((math.log(self.info[1]+1)/(son.info[1]+0.1))**0.5)
            #print(score, son.point)
            if score > best_score:
                best_score = score
                best_son = son
        return best_son
    def move(self, point):
        for son in self.son:
            if son.point == point:
                return son
        return None
    def HugeSon(self):
        best_score = -1
        best_son = None
        for son in self.son:
            score = son.info[1]
            #print(score, son.point)
            if score > best_score:
                best_score = score
                best_son = son
        return best_son
class ai_mtcl(ai_base):
            
    def __init__(self, size, K=1.5, T = 100000, name='ai_montocalo'):
        super().__init__(size, name)
        self.K = K
        self.T = T
        self.tree = None
        self.board = Chessboard(size)
    def reset(self, color):
        self.color = color
        self.tree = None
        self.board.reset()
    def step(self, chessboard, lastMove, result):
        if result != 0:
            return None
        if lastMove == None:
            self.board.step(self.color, ((self.size)//2,(self.size)//2))
            return ((self.size)//2,(self.size)//2)
        if self.tree == None:
            self.board.set(chessboard)
            self.tree = tree_node(None, calc_av(chessboard, None, set()), self.K)
            #print(self.tree.ava)
        else:
            #print(lastMove)
            son = self.tree.move(lastMove[1])
            if son == None:
                self.board.set(chessboard)
                self.tree = tree_node(None, calc_av(chessboard, None, set()), self.K)
            else:
                print('reuse success')
                self.board.step(3-self.color, lastMove[1])
                self.tree = son
        t = time.time()
        for i in range(self.T):
            #print('i =', i)
            if time.time()-t > 5:
                print('run %d iters' % (i+1))
                for son in self.tree.son:
                    print('\t', son.point, son.info)
                break
            current_node = self.tree
            board = self.board.copy()
            color = self.color
            path = [current_node]
            while current_node.flag == 0 and current_node.son != None:
                next_node = current_node.bestSon()
                path.append(next_node)
                point = next_node.point
                board[point[0]][point[1]] = color
                color = 3-color
                current_node = next_node
            if current_node.flag != 0:
                #print('over = ', current_node.flag)
                res = current_node.flag
                add_res = [0 if (res == color) else 1, 1 if (res == color) else 0]
                if res == -1:
                    add_res = [0.5, 0.5]
                for i, node in enumerate(path):
                    node.info[0] += add_res[i % 2]
                    node.info[1] += 1                
                continue
            #for p in path:
            #    print('\t', p.point, p.flag)
            current_node = current_node.addSon(board, color)
            point = current_node.point
            board[point[0]][point[1]] = color
            color = 3-color            
            path.append(current_node)
            res = random_walk(board, color, current_node.ava)
            add_res = [0 if (res == color) else 1, 1 if (res == color) else 0]
            if res == -1:
                add_res = [0.5, 0.5]
            for i, node in enumerate(path):
                node.info[0] += add_res[i % 2]
                node.info[1] += 1
            
            
            
        ret = self.tree.HugeSon().point
        self.tree = self.tree.move(ret)
        self.board.step(self.color, ret)
        print('predict')
        for son in self.tree.son:
            print('\t', son.point, son.info)
        return ret