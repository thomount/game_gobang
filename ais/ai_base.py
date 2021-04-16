class ai_base:
    # pure random
    def __init__(self, size, name='human'):
        self.size = size
        self.name = name
    def reset(self, color):
        # set color
        self.color = color
    def step(self, chessboard, lastMove, result):
        # result: current isWin result
        # return next move
        s = input().split()
        x, y = int(s[0]), int(s[1])
        return (x, y)
    def load_model(self, f):
        pass