from classes.Signals import RectangleSignal, SineSignal, TriangleSignal
from classes.StateSpaceSystem import StateSpaceSystem
from classes.SystemSimulation import SystemSimulation

step_size = None #fill that
J1 = None #fill that
J2 = None #fill that
n1 = None #fill that
n2 = None #fill that
k = None #fill that
b = None #fill that
Jeq = J2 + J1 * pow(n2/n1, 2)
tolerance = None # fill that

state_matrix = [[0, 1],[-k/Jeq, -b/Jeq]]
input_matrix = [[0], [n2/(n1*Jeq)]]
output_matrix = [[1, 0], [0, 1]]

inital_state = [[None], [None]]



system = StateSpaceSystem(state_matrix, input_matrix, output_matrix, inital_state)
simulation = SystemSimulation(step_size, system)


