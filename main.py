import numpy as np

from classes.StateSpaceSystem import StateSpaceSystem
from classes.SystemSimulation import SystemSimulation

state_matrix = np.array([
    [0, 1],
    [-10, 0]])
input_matrix = np.array([
    [0],
    [1]])
output_matrix = np.array(
    [[1, 0],
     [0, 1]])
initial_state = np.array(
    [[0.2],
     [0.0]])
u = np.array([[0.0]])

Environment = SystemSimulation()
System = StateSpaceSystem(state_matrix, input_matrix, output_matrix, initial_state)

Environment.run(System, u, 2)

print(Environment)

Environment.plot_system()