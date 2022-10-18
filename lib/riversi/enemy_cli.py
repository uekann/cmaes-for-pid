import random
from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
from time import sleep

from .borad_cli import RiversiBoard, BitBoard


class BaseEnemy(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, color:int) -> None:
        self.color = color
    
    @abstractmethod
    def action(self, rb:"RiversiBoard") -> tuple:
        pass


class RandomEnemy(BaseEnemy):
    def __init__(self, color: int, delay:int = 0) -> None:
        super().__init__(color)
        self.delay = delay
    
    def action(self, rb: "RiversiBoard") -> tuple:
        places = rb.get_places_to_put(self.color)
        assert places.count_bit() > 0
        
        sleep(self.delay)
        
        if places.count_bit() == 1:
            return list(places)[0]
        return list(places)[random.randint(0, places.count_bit()-1)]
    

class LearnedEnemy(BaseEnemy):
    def __init__(self, color:int, gen:int) -> None:
        super().__init__(color)
        df = pd.read_csv("/Users/uekann/Desktop/VSCodeProjects/CMA-ES/pid/model/learn_data.csv")
        self.w = df[gen:gen+1].values[0][1:]

    
    def action(self, rb: "RiversiBoard") -> tuple:
        
        assert rb.get_places_to_put(self.color).count_bit() > 0
        max_e = -float("inf")
        best_p = ()
        for p in rb.get_places_to_put(self.color):
            new_bd = RiversiBoard(rb[self.color], rb[RiversiBoard.turn_color(self.color)])
            new_bd.put(RiversiBoard.BLACK, p)
            env_vec = np.zeros(128, np.int32)
            env_vec[:64] = new_bd[RiversiBoard.BLACK].to_ndarray().flatten()
            env_vec[64:] = new_bd[RiversiBoard.WHITE].to_ndarray().flatten()
            e = np.dot(env_vec, self.w)
            if e > max_e:
                best_p = p
                max_e = e
        
        return best_p

def main():
    LearnedEnemy(0)