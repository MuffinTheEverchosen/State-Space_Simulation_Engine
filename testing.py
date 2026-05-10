import numpy as np

from classes.Signals import RectangleSignal, SineSignal, TriangleSignal
from classes.StateSpaceSystem import StateSpaceSystem
from classes.SystemSimulation import SystemSimulation
step_size = 0.01

Feedthrough_System = StateSpaceSystem([[0, 0],[0, 0]], [[0],[0]], [[0, 0],[0, 0]], [[10.0], [0.0]], [[1.0], [0.0]])
Perfect_Oscillator_System = StateSpaceSystem([[0, 1], [-10, 0]], [[0],[1]], [[1, 0],[0, 1]], [[0.2],[0.0]])
Square_Signal = RectangleSignal(10, 8)
Sine_Signal = SineSignal(8, 8)
Triangle_Signal = TriangleSignal(8, 8)

Feedthrough_Env = SystemSimulation(step_size, Feedthrough_System, False, True)
Feedthrough_Env.run([[Triangle_Signal]], 20)

Feedthrough_Env.plot_results()

print(Feedthrough_Env)