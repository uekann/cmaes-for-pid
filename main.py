import numpy as np
from matplotlib import pyplot as plt

from simulate import SecondOrderSystem, PID
from cmaes import CMAES



def evaluate(x):
    y = 0
    controler = PID(*x)
    tf = SecondOrderSystem(time=50)
    r = 0
    for i in range(499):
        u = controler.cal_next_input(10-y)
        y = tf.response(u)
    
    return np.sum(np.tanh(np.abs(10 - tf.y[:,0])))


es = CMAES(func=evaluate,\
            init_mean=np.array([0.0, 0.0, 0.0]),\
            init_sigma=10,\
            nsample=100)

mean = np.zeros(3000, dtype=np.float64)

for i in range(3000):
    es.sample()
    es.evaluate()
    es.update_param()
    mean[i] = es.func(es.mean)

print(es.mean)

controler = PID(*es.mean)
tf = SecondOrderSystem(time=50)
y = 0
for i in range(499):
    u = controler.cal_next_input(10-y)
    y = tf.response(u)

plt.figure(figsize=(10,5))

plt.subplot(121)
plt.title("Transition of evaluation function")
plt.semilogy(mean)
plt.ylim(np.min(mean),np.max(mean[500:]))
plt.xlabel("number of iterations")
plt.ylabel("loss function")
plt.grid()
plt.legend()

plt.subplot(122)
plt.title("PID simulation with second-order system")
plt.plot(np.linspace(0, 50, 500), tf.y[:,0])

plt.show()