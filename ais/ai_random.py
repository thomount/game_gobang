from .ai_base import ai_base
import random
class ai_random(ai_base):
    def __init__(self, size):
        super().__init__(size)
    def step(self, chessboard, lastMove, result):
        pool = []
        for i in range(self.size):
            for j in range(self.size):
                if chessboard[i][j] == 0:
                    pool.append((i, j))
        return random.choice(pool)
    
class ai_random_near(ai_base):
    def __init__(self, size):
        super().__init__(size)
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
                        pool.append((i, j))
        return random.choice(pool)
    
        