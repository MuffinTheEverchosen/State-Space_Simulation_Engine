import numpy as np

from classes.StateSpaceSystem import StateSpaceSystem
from classes.SystemSimulation import SystemSimulation

A = np.array([[0.0, 0.1], [-1.0, 0.0]])
B = np.array([[0.0], [1.0]])
C = np.array([[1.0, 0.0]])

x0 = np.array([[1.0], [0.0]])
u = np.array([[0.0]])
step_size = 0.1

Environment = SystemSimulation(step_size)
System = StateSpaceSystem(A, B, C, x0)

while Environment.current_time < 20:
    Environment.step(System, u)

print(Environment)