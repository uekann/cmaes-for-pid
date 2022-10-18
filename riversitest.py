import numpy as np
from matplotlib import pyplot as plt

from lib.cmaes import CMAES
from lib.riversi import RiversiBoard, GameEnv, random_choice


def evaluate(x:np.ndarray):
    score = 0
    for i in range(100):
        if i%2:
            color = RiversiBoard.BLACK
        else:
            color = RiversiBoard.WHITE
        
        
        game = GameEnv(random_choice, color)
        
        while True:
            mb, yb, fin = game.get_env()
            if fin: break
            now = RiversiBoard(mb, yb)
            
            max_e = -float("inf")
            best_p = ()
            for p in now.get_places_to_put():
                next_bd = RiversiBoard(mb, yb).put(RiversiBoard.BLACK, p)
                env_vec = np.zeros(128, np.int32)
                env_vec[:64] = (next_bd == RiversiBoard.BLACK).flatten()+0
                env_vec[64:] = (next_bd == RiversiBoard.WHITE).flatten()+0
                e = np.dot(env_vec, x)
                if e > max_e:
                    best_p = p
                    max_e = e
            
            game.put(best_p)
        
        score += game.score()
    
    return score/100

es = CMAES(func=evaluate,\
            init_mean=np.zeros(128),\
            init_sigma=10,\
            nsample=10)

mean = np.zeros(100, dtype=np.float64)

for i in range(500):
    es.sample()
    es.evaluate()
    es.update_param()
    mean[i] = es.func(es.mean)
    if np.all(es.sigma*np.sqrt(es.D) < 1e-10):
        break

print(es.mean)