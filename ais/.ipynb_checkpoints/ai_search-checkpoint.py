import sys, os
sys.path.append("..")
from common import *
from ais.ai_base import ai_base
import random
def estimate(chessboard, color):   # color's turn to move
    score = [0.5, 0.5]
    win_flag = chessboard.isWin()
    if win_flag in [1, 2]:
        score[win_flag-1] = 1.01
        score[2-win_flag] = -0.01
        return score
    
    size = chessboard.size
    wc = [0, 0]

    for i in range(size):
        for j in range(size):
            if chessboard[i][j] == 0:
                exist_flag = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        i1 = i+dx
                        j1 = j+dy
                        if (dx != 0 or dy != 0) and chessboard.isLegal((i1, j1)) and not chessboard.isEmpty((i1, j1)):
                            exist_flag = 1
                            break
                if exist_flag == 1:
                    ldir = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
                    rdir = [(1, 0), (1, 1), (0, 1), (-1, 1)]
                    for c in range(1, 3):
                        wc_flag = 0
                        for d in range(4):
                            count = 1
                            for step in range(1, 5):
                                pos = (i+ldir[d][0]*step, j+ldir[d][1]*step)
                                if chessboard.isLegal(pos) and chessboard[pos[0]][pos[1]] == c:
                                    count += 1
                                else:
                                    break
                            for step in range(1, 5):
                                pos = (i+rdir[d][0]*step, j+rdir[d][1]*step)
                                if chessboard.isLegal(pos) and chessboard[pos[0]][pos[1]] == c:
                                    count += 1
                                else:
                                    break
                            #print(i, j, count)
                            if count >= 5:
                                wc_flag = 1
                                break
                        if wc_flag == 1:
                            wc[c-1] += 1
    #print(wc)
    if wc[color-1] > 0:
        score[color-1] = 1
        score[2-color] = 0
    elif wc[2-color] > 1:
        score[color-1] = 0
        score[2-color] = 1
    return score

class ai_search(ai_base):
    def __init__(self, size, name='ai_search'):
        super().__init__(size, name)
    def step(self, chessboard, lastMove, result):
        if result != 0:
            return None
        if lastMove == None:
            return ((self.size)//2,(self.size)//2)
        res = self.search(chessboard, 3, self.color)
        return res[1]
    def search(self, chessboard, depth, color):
        if chessboard.isWin() == -1:
            return 0.5, None
        pool = []
        for i in range(self.size):
            for j in range(self.size):
                if chessboard[i][j] == 0:
                    exist_flag = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            i1 = i+dx
                            j1 = j+dy
                            if (dx != 0 or dy != 0) and chessboard.isLegal((i1, j1)) and not chessboard.isEmpty((i1, j1)):
                                exist_flag = 1
                                break
                    if exist_flag == 1:
                        chessboard[i][j] = color
                        score = estimate(chessboard, 3-color)
                        chessboard[i][j] = 0
                        pool.append([i, j, score[color-1]])
                        
        pool.sort(key=lambda x: -x[2])
        if depth == 0 or pool[0][-1] >= 1:
            return 1-pool[0][-1], pool[0][:-1]
        
        while pool[-1][2] != pool[0][2]:
            pool = pool[:-1]
        
        min_score = 3
        best_move = None
        random.shuffle(pool)
        for pos in pool[:min(len(pool), 10)]:
            chessboard[pos[0]][pos[1]] = color
            #print('d%d : try (%d, %d)' % (depth, pos[0], pos[1]))
            ret = self.search(chessboard, depth-1, 3-color)
            chessboard[pos[0]][pos[1]] = 0
            move, res = ret[1], 1-ret[0]
            if res < min_score:
                min_score = res
                best_move = (pos[0], pos[1])
                if min_score <= 0:
                    break
        return min_score, best_move
            
class ai_search_q(ai_base):
    def __init__(self, size, name='ai_search_quick'):
        super().__init__(size, name)
    def step(self, chessboard, lastMove, result):
        if result != 0:
            return None
        if lastMove == None:
            return ((self.size)//2,(self.size)//2)
        ava = set()
        for i in range(self.size):
            for j in range(self.size):
                if chessboard[i][j] == 0:
                    exist_flag = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            i1 = i+dx
                            j1 = j+dy
                            if (dx != 0 or dy != 0) and chessboard.isLegal((i1, j1)) and not chessboard.isEmpty((i1, j1)):
                                exist_flag = 1
                                break   
                    if exist_flag == 1:
                        ava.add((i, j))
                        
        res = self.search(chessboard, 3, self.color, ava)
        return res[1]
    def estimate(self, chessboard, color, ava):  # color先手的胜率
        score = 0.5
        size = chessboard.size
        wc = [0, 0]

        for P in ava:
            i, j = P[0], P[1]
            ldir = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
            rdir = [(1, 0), (1, 1), (0, 1), (-1, 1)]
            for c in range(1, 3):
                wc_flag = 0
                for d in range(4):
                    count = 1
                    for step in range(1, 5):
                        pos = (i+ldir[d][0]*step, j+ldir[d][1]*step)
                        if chessboard.isLegal(pos) and chessboard[pos[0]][pos[1]] == c:
                            count += 1
                        else:
                            break
                    for step in range(1, 5):
                        pos = (i+rdir[d][0]*step, j+rdir[d][1]*step)
                        if chessboard.isLegal(pos) and chessboard[pos[0]][pos[1]] == c:
                            count += 1
                        else:
                            break
                    #print(i, j, count)
                    if count >= 5:
                        wc_flag = 1
                        break
                if wc_flag == 1:
                    wc[c-1] += 1
        #print(wc)
        if wc[color-1] > 0:
            return 0.99999
        elif wc[2-color] > 1:
            return 0.00001
        return score
    def new_ava(self, chessboard, ava, pos):
        ret = ava.copy()
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                x = pos[0]+i
                y = pos[1]+j
                if chessboard.isLegal((x, y)) and chessboard.isEmpty((x, y)):
                    ret.add((x, y))
        ret.remove(pos)
        return ret
    def estimate_point(self, chessboard, P, color):
        i, j = P[0], P[1]
        ldir = [(-1, 0), (-1, -1), (0, -1), (1, -1)]
        rdir = [(1, 0), (1, 1), (0, 1), (-1, 1)]
        score = 0
        for c in range(1, 3):
            K = 1
            if c != color: K += 0.5
            for d in range(4):
                count = 2
                plus = 2
                for step in range(1, 5):
                    pos = (i+ldir[d][0]*step, j+ldir[d][1]*step)
                    if chessboard.isLegal(pos):
                        if chessboard[pos[0]][pos[1]] == c:
                            count += plus
                        elif chessboard.isEmpty(pos):
                            plus >>= 1
                            count += plus
                        else:
                            break
                    else:
                        break
                plus = 2
                for step in range(1, 5):
                    pos = (i+rdir[d][0]*step, j+rdir[d][1]*step)
                    if chessboard.isLegal(pos):
                        if chessboard[pos[0]][pos[1]] == c:
                            count += plus
                        elif chessboard.isEmpty(pos):
                            plus >>= 1
                            count += plus
                        else:
                            break
                    else:
                        break
                score += K*(3**count)
        return score
    def search(self, chessboard, depth, color, available): # color 走的先手胜率
        win_flag = chessboard.isWin()
        if win_flag != 0:
            if win_flag == -1:
                return 0.5, None
            elif win_flag == color:
                return 1, None
            else:
                return 0, None
        if depth == 0:
            return self.estimate(chessboard, color, available), None
    
        pool = []
        for pos in available:
            pool.append((pos, self.estimate_point(chessboard, pos, color)))
        pool.sort(key=lambda x: -x[1])
        if len(pool) > 10:
            pool = pool[:10]
        min_score = 3
        best_move = None
        for item in pool:
            pos = item[0]
            chessboard[pos[0]][pos[1]] = color
            #print('d%d : try (%d, %d)' % (depth, pos[0], pos[1]))
            ret = self.search(chessboard, depth-1, 3-color, self.new_ava(chessboard, available, pos))
            chessboard[pos[0]][pos[1]] = 0
            move, res = ret[1], ret[0]
            if res < min_score:
                min_score = res
                best_move = (pos[0], pos[1])
                if min_score <= 0:
                    break
        return 1-min_score, best_move

if __name__ == '__main__':
    chess = Gobang_board(GB_size)
    print(chess.step(1, (5,5)))
    print(chess.step(1, (6,6)))
    print(chess.step(1, (7,7)))
    print(chess.step(1, (8,8)))
    print(chess.step(2, (9,9)))
    print(estimate(chess, 1))
    print(estimate(chess, 2))
    ai = ai_search_q(GB_size)
    ai.reset(1)
    print(ai.step(chess, [0,0], 0))