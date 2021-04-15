from .ai_base import ai_base
import random
def estimate(chessboard):
    score = [0,0]
    win_flag = chessboard.isWin()
    if win_flag in [1, 2]:
        score[win_flag-1] = 1e8
        score[2-win_flag] = -1e8
    
    return score

class ai_greedy(ai_base):
    def __init__(self, size, name='ai_greedy'):
        super().__init__(size, name)
    def step(self, chessboard, lastMove, result):
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
                        virtual_board = chessboard.copy()
                        virtual_board.step(self.color, (i, j))
                        score = estimate(virtual_board)
                        pool.append([i, j, score[self.color-1]])
                        
        pool.sort(key=lambda x: -x[2])
        while pool[-1][2] != pool[0][2]:
            pool = pool[:-1]
        return tuple(random.choice(pool)[:-1])
        
    
        