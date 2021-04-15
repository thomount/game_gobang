import common as cm
from ais.ai_random import ai_random as AI_1
from ais.ai_random import ai_random_near as AI_2

class Game:
    def __init__(self):
        self.board = cm.Gobang_board()
        self.size = self.board.size
        
    def start(self, ai_1, ai_2, flag):
        ai_1.reset(1)
        ai_2.reset(2)
        self.AIs = [ai_1, ai_2]
        self.board.reset()
        turn_n = 0
        while self.board.isWin() == 0:
            next_ai = self.AIs[turn_n % 2]    
            nextPos = next_ai.step(self.board, self.board.history[-1] if len(self.board.history) > 0 else None, self.board.isWin())
            if not self.board.step(turn_n%2+1, nextPos):
                print("player", turn_n%2+1, 'make a wrong move on', nextPos)
                break
            turn_n += 1
            if flag == True:
                self.board.show()
                print()
        result = self.board.isWin()    
        ai_1.step(self.board, self.board.history[-1], result)
        ai_2.step(self.board, self.board.history[-1], result)
        if flag == True:
            if result == -1:
                print('tie!')
            if result in [1, 2]:
                print('player', result, 'win!')
            if result == 0:
                print('game over illegally...')

        return result
        
if __name__ == '__main__':
    game = Game()
    ai_1 = AI_1(cm.GB_size)
    ai_2 = AI_2(cm.GB_size)
    #game.start(ai_1, ai_2, True)
    count = [0,0]
    for i in range(100):
        res = game.start(ai_1, ai_2, False)
        if res == -1:
            count[0] += 1
            count[1] += 1
        elif res in [1, 2]:
            count[res-1] += 3
        print('rount %d finish' % (i+1))
    print(f'100 round score: %.2f : %.2f' % (count[0]/(count[0]+count[1])*100, count[1]/(count[0]+count[1])*100))
        
    