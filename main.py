import numpy as np

from classes.Signals import SquareSignal
from classes.StateSpaceSystem import StateSpaceSystem
from classes.SystemSimulation import SystemSimulation
step_size = 0.01



# Testing

Feedthrough_System = StateSpaceSystem([[0, 0],[0, 0]], [[0],[0]], [[0, 0],[0, 0]], [[0.0], [0.0]], [[1.0], [0.0]])
Perfect_Oscillator_System = StateSpaceSystem([[0, 1], [-10, 0]], [[0],[1]], [[1, 0],[0, 1]], [[0.2],[0.0]])
Square_Signal = SquareSignal(10, 50)

Feedthrough_Env = SystemSimulation(step_size, Feedthrough_System)
Feedthrough_Env.run([[Square_Signal]], 200)

Feedthrough_Env.plot_results()

print(Feedthrough_Env)