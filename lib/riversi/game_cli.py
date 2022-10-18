from .borad_cli import RiversiBoard
from .enemy_cli import BaseEnemy, LearnedEnemy, RandomEnemy


class GameEnv:
    
    def __init__(self, enemy:"BaseEnemy", color:int = RiversiBoard.BLACK) -> None:
        self._board = RiversiBoard()
        self._turn = RiversiBoard.BLACK
        self.enemy = enemy
        self._count = 0
        self.color = color
        self._end = False
        
    
    @property
    def end(self):
        return self._end


    @property
    def board(self):
        return self._board
    
    @property
    def turn(self):
        return self._turn
    
    @property
    def count(self):
        return self._count
        
    
    def get_env(self) -> tuple:
        if not self._board.is_end() :self.update()
        return (self.board[self.color],
                self.board[RiversiBoard.turn_color(self.color)], self._board.is_end())
    
    
    def update(self) -> bool:
        if self.turn != RiversiBoard.turn_color(self.color):
            return False
        
        self._turn = self.color
        if not self._board.get_places_to_put(RiversiBoard.turn_color(self.color)):
            return False
        
        if self._board.put(RiversiBoard.turn_color(self.color),self.enemy.action(self._board)):
            self._count += 1
            return True
        
        return False
    
    
    def put(self, place:tuple) -> bool:
        if self._turn != self.color:
            return False
        
        self._turn = RiversiBoard.turn_color(self.color)
        
        if place == (-1, -1):
            self._count += 1
            return False
        
        if self._board.put(self.color, place):
            self._count += 1
            return True
        
        
        return False
    
    
    def score(self):
        scores = self._board.get_scores()
        gap = scores[self.color] - scores[RiversiBoard.turn_color(self.color)]
        return gap*(0.99**self._count)


def main():
    game = GameEnv(LearnedEnemy(RiversiBoard.WHITE, 0))
    while True:
        b1, b2, fin = game.get_env()
        if fin: break
        print(game.board)
        print(game.board.get_places_to_put(RiversiBoard.BLACK))
        p = tuple(map(int, input("place : ").split()))
        game.put(p)
    
    print(game.board)