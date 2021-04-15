class ai_base:
    # pure random
    def __init__(self, size):
        self.size = size
    def reset(self, color):
        # set color
        self.color = color
    def step(self, chessboard, lastMove, result):
        # result: current isWin result
        # return next move
        pass
    def load_model(self, f):
        pass