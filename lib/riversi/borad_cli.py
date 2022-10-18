from copy import deepcopy
import numpy as np

class BitBoard(int):
    def __init__(self, bb = 0) -> None:
        self = bb & 0xffffffffffffffff
    
    def to_ndarray(self) -> np.ndarray:
        b = self
        arr = []
        for _ in range(8):
            l = [0]*8
            for i in range(8):
                if b & 1:
                    l[i] = 1
                b = b>>1
            arr.append(l)
        return np.array(arr, dtype=np.int32)
    
    def count_bit(self):
        mask = 0x8000000000000000
        count = 0

        for _ in range(64):
            if mask&self:
                count += 1
            mask = mask>>1
        
        return count

    
    def __str__(self) -> str:
        return " ".join(map(str, self))
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __and__(self, __n: int) -> 'BitBoard':
        return BitBoard(super().__and__(__n))
    
    def __or__(self, __n: int) -> 'BitBoard':
        return BitBoard(super().__or__(__n))
    
    def __xor__(self, __n: int) -> 'BitBoard':
        return BitBoard(super().__xor__(__n))
    
    def __lshift__(self, __n: int) -> 'BitBoard':
        return BitBoard(super().__lshift__(__n))

    def __rshift__(self, __n: int) -> 'BitBoard':
        return BitBoard(super().__rshift__(__n))
    
    def __invert__(self) -> 'BitBoard':
        return BitBoard(0xffffffffffffffff-self)
    
    
    def __iter__(self):
        p = 1
        for i in range(8):
            for j in range(8):
                if self & p:
                    yield (i, j)
                p = p<<1
        return
    
    @classmethod
    def list_to_bitboard(cls, l:list):
        bb = BitBoard()
        for li in l:
            bb = bb | (1<<(li[0]*8+li[1]))
        return bb
    
    @classmethod
    def ndarray_to_bitboard(cls, arr:np.ndarray):
        bb = BitBoard()
        for i in range(8):
            for j in range(8):
                if arr[i,j] == 1:
                    bb = bb | (1<<(i*8+j))
        return bb



class RiversiBoard:
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    def __init__(self, bb=None, bw=None):
        
        if not(bb is None or bw is None):
            if isinstance(bb, int) and isinstance(bw, int):
                self._board = {RiversiBoard.BLACK:BitBoard(bb), RiversiBoard.WHITE:BitBoard(bw)}
            else:
                raise TypeError()

        else:
            self._board = {RiversiBoard.BLACK:BitBoard(0x0000000810000000), RiversiBoard.WHITE:BitBoard(0x0000001008000000)}
    
    
    @property
    def board(self):
        return self._board

        
    @classmethod
    def turn_color(cls, color:int) -> int:
        if color == RiversiBoard.BLACK:
            return RiversiBoard.WHITE
        elif color == RiversiBoard.WHITE:
            return RiversiBoard.BLACK
        else:
            return None
    

    @classmethod
    def ndarray_to_board(cls, arr:np.ndarray) -> 'RiversiBoard':
        bb = BitBoard.ndarray_to_bitboard(arr==RiversiBoard.BLACK)
        bw = BitBoard.ndarray_to_bitboard(arr==RiversiBoard.WHITE)
        return RiversiBoard(bb=bb,bw=bw)

    
    def to_ndarray(self) -> np.array:
        arr = np.zeros((8,8),dtype=np.int32)
        arr += self._board[RiversiBoard.BLACK].to_ndarray() * RiversiBoard.BLACK
        arr += self._board[RiversiBoard.WHITE].to_ndarray() * RiversiBoard.WHITE
        return arr


    def get_places_to_put(self, color:int) -> 'BitBoard':
        b1 = self._board[color]
        b2 = self._board[RiversiBoard.turn_color(color)]

        bl = ~(b1 | b2)
        lr = ~BitBoard(0b1000000110000001100000011000000110000001100000011000000110000001)
        ud = ~BitBoard(0b1111111100000000000000000000000000000000000000000000000011111111)
        sr = ~BitBoard(0b1111111110000001100000011000000110000001100000011000000111111111)

        ret = BitBoard()

        for dir, mask in [(8, ud), (9, sr), (1, lr), (7, sr)]:
            tmp = b1
            for _ in range(6):
                tmp = tmp | ((b2 & mask) & (tmp >> dir))
            ret = ret | (((tmp & ~b1) >> dir) & bl)

            tmp = b1
            for _ in range(6):
                tmp = tmp | ((b2 & mask) & (tmp << dir))
            ret = ret | (((tmp & ~b1) << dir) & bl)

        return ret
    

    def get_change_places(self, color:int, place:tuple) -> 'BitBoard':
        b1 = self._board[color]
        b2 = self._board[RiversiBoard.turn_color(color)]
        
        p = BitBoard(1<<(place[0]*8 + place[1]))
        if p & (b1|b2):
            return BitBoard(0)

        lr = ~BitBoard(0b1000000110000001100000011000000110000001100000011000000110000001)
        ud = ~BitBoard(0b1111111100000000000000000000000000000000000000000000000011111111)
        sr = ~BitBoard(0b1111111110000001100000011000000110000001100000011000000111111111)

        ret = BitBoard()

        for dir, mask in [(8, ud), (9, sr), (1, lr), (7, sr)]:
            tmp = p
            for _ in range(6):
                tmp = tmp | ((b2 & mask) & (tmp >> dir))
                if (tmp>>dir)&b1:
                    break
            else:
                tmp = 0
            ret = ret | (tmp & ~p)


            tmp = p
            for _ in range(6):
                tmp = tmp | ((b2 & mask) & (tmp << dir))
                if (tmp<<dir)&b1:
                    break
            else:
                tmp = 0
            ret = ret | (tmp & ~p)
        
        return ret
    

    def put(self, color:int, place:tuple) -> bool:

        change_place = self.get_change_places(color, place)
        if not change_place:
            return False

        self._board[RiversiBoard.BLACK] = self._board[RiversiBoard.BLACK]^change_place
        self._board[RiversiBoard.WHITE] = self._board[RiversiBoard.WHITE]^change_place

        self._board[color] = self._board[color] | (1<<(place[0]*8+place[1]))

        return True


    def __str__(self) -> str:
        s = ""
        for i in self.to_ndarray():
            s += " ".join(map(str, i)) + "\n"
        return s
    
    
    def __getitem__(self, color):
        if not (color==RiversiBoard.WHITE or color==RiversiBoard.BLACK):
            raise ValueError(f"Color must be {RiversiBoard.BLACK} or {RiversiBoard.WHITE} but {color} was given")
        
        return self._board[color]

    def get_scores(self) -> dict:
        return {RiversiBoard.BLACK : self._board[RiversiBoard.BLACK].count_bit(),
                RiversiBoard.WHITE : self._board[RiversiBoard.WHITE].count_bit()}
    
    
    def is_end(self) -> bool:
        return not bool(self.get_places_to_put(RiversiBoard.WHITE) | self.get_places_to_put(RiversiBoard.BLACK))


def main():
    rb = RiversiBoard()
