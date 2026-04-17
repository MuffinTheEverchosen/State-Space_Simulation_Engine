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
step_size = 0.1

System = StateSpaceSystem(state_matrix, input_matrix, output_matrix, initial_state)
Environment = SystemSimulation(step_size, System)