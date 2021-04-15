map = ['.', '#', 'O']
GB_size = 15
class Chessboard:
    def __init__(self, size=GB_size):
        self.size = size
        self.board = [[0 for i in range(size)] for j in range(size)]
        self.history = []
    def isLegal(self, pos):
        return (0 <= pos[0] and pos[0] < self.size and 0 <= pos[1] and pos[1] < self.size)
    def isEmpty(self, pos):
        return (self.board[pos[0]][pos[1]] == 0)
    def step(self, flag, pos):
        if self.isLegal(pos) and self.isEmpty(pos) and (flag in [1, 2]):
            self.board[pos[0]][pos[1]] = flag
            self.history.append((flag, pos))
            return True
        else:
            return False
    def reset(self):
        self.board = [[0 for i in range(self.size)] for j in range(self.size)]
    def show(self, zoom=1):
        for i in range(self.size):
            for k in range(zoom):
                for j in range(self.size):
                    print(map[self.board[i][j]]*zoom, end=' '*(zoom-1))
                print()
            for k in range(zoom-1):
                print()
            
    def copy(self):
        ret = self.__class__(self.size)
        ret.history = []
        for i in range(self.size):
            for j in range(self.size):
                ret.board[i][j] = self.board[i][j]
        return ret
    def build_from_file(self, f):
        #TODO
        pass
    
    def __getitem__(self, x):
        return self.board[x]
class Gobang_board(Chessboard):
    def __init__(self, size=GB_size):
        super().__init__(size)
    def isWin(self):
        # 0 for not yet, 1 for 1 win, 2 for 2 win, -1 for tie
        # TODO logic check
        full_flag = 1
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    full_flag = 0
                else:
                    dirs = [(-1, 1), (0, 1), (1, 1), (1, 0)]
                    start_color = self.board[i][j]
                    for dir in dirs:
                        combo_flag = 1
                        for step in range(1, 5):
                            next_pos = (i+dir[0]*step, j+dir[1]*step)
                            if not self.isLegal(next_pos) or self.board[next_pos[0]][next_pos[1]] != start_color:
                                combo_flag = 0
                                break
                        if combo_flag == 1:
                            #print((i, j), dir)
                            return start_color
        if full_flag == 1:
            return -1
        
        return 0
            
if __name__ == '__main__':
    chess = Gobang_board(GB_size)
    print(chess.step(1, (7,7)))
    print(chess.step(2, (8,8)))
    chess.show()
        