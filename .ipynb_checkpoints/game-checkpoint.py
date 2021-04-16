import common as cm
import ai_menu as ai
import time

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
        using_time = [0,0]
        while self.board.isWin() == 0:
            next_ai = self.AIs[turn_n % 2]    
            using_time[turn_n%2] -= time.time()
            nextPos = next_ai.step(self.board, self.board.history[-1] if len(self.board.history) > 0 else None, self.board.isWin())
            using_time[turn_n%2] += time.time()
            if not self.board.step(turn_n%2+1, nextPos):
                print("player", turn_n%2+1, 'make a wrong move on', nextPos)
                break
            turn_n += 1
            #print(turn_n, nextPos)
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
        self.detail = [result, turn_n, self.board, using_time]
        return result
        
if __name__ == '__main__':
    game = Game()

    def single_game(l, r):
        game.start(l, r, True)

    def multi_game(l, r):
        count = [0,0]
        for i in range(20):
            res = game.start(l, r, False)
            if res == -1:
                count[0] += 1
                count[1] += 1
            elif res in [1, 2]:
                count[res-1] += 3
            print('rount %d-1 finish, winner is %d in %d steps' % (i+1, res, game.detail[1]))
            print('time: %.2f %.2f' % (game.detail[3][0], game.detail[3][1]))
            game.detail[2].show()

            res = game.start(r, l, False)
            if res == -1:
                count[0] += 1
                count[1] += 1
            elif res in [1, 2]:
                count[2-res] += 3
            print('rount %d-2 finish, winner is %d in %d steps' % (i+1, 3-res, game.detail[1]))
            print('time: %.2f %.2f' % (game.detail[3][1], game.detail[3][0]))
            game.detail[2].show()

        print(f'20 round score: %.2f : %.2f' % (count[0]/(count[0]+count[1])*100, count[1]/(count[0]+count[1])*100))
        
    l = ai.get_AI(0)
    r = ai.get_AI(4)
    #multi_game(l, r)
    single_game(l, r)
        
    