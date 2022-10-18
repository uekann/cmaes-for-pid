import numpy as np
from matplotlib import pyplot as plt


class SecondOrderSystem:

    def __init__(self, time=100, dt=0.1, k=1, zeta=0.7, omega=4):
        self.time = time
        self.dt = dt
        self.a0 = 1 / k
        self.a2 = self.a0 / (omega**2)
        self.a1 = zeta * 2 * np.sqrt(self.a0 * self.a2)

        self.y = np.zeros((int(time/dt),3))
        self.u = np.zeros(int(time/dt))

        self.step = 0
    
    def response(self, u):
        self.u[self.step] = u
        self.y[self.step, 2] = u - self.a0*self.y[self.step,0] - self.a1*self.y[self.step,1]
        self.y[self.step+1, 1] = self.y[self.step, 1] + self.dt * self.y[self.step,2]
        self.y[self.step+1, 0] = self.y[self.step, 0] + self.dt * self.y[self.step,1]
        ret = self.y[self.step, 0]
        self.step += 1
        return ret
    

    def result(self):
        plt.plot(np.linspace(0,self.time,int(self.time/self.dt)), self.y[:,0])


class SecondOrderSystemVec:

    def __init__(self, time=100, dt=0.1, k=1, zeta=0.7, omega=0.4) -> None:
        self.time = time
        self.dt = dt

        self.x = np.zeros((int(time/dt),2))
        self.xdot = np.zeros((int(time/dt),2))

        self.u



class PID:

    def __init__(self, kp=1.58657748, ki=0.16824089, kd=15.07412643):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.sum = 0
        self.last = 0

    def cal_next_input(self, e):
        self.sum += e

        p = self.kp * e
        i = self.ki * self.sum
        d = self.kd * (e - self.last)

        self.last = e
        return p+i+d


def main():
    # controler = PID()
    u = np.zeros(1000)
    u[0] = 10
    tf = SecondOrderSystem()

    y = 0
    target = 1

    for i in range(999):
        # u = controler.cal_next_input(target-y)
        y = tf.response(u[i])
    
    print(np.sum((10 - tf.y[10:,0])**2) + np.max(tf.y[:,2]**2))
    tf.result()
    plt.show()