import numpy as np

from Utilities.types import Matrix, Vector


class StateSpaceSystem:
    def __init__(self, state_matrix: Matrix, input_matrix: Matrix, output_matrix: Matrix, initial_state: Vector, feedthrough_matrix: Matrix = np.array([[0.0]]), initial_time: float = 0):
        self.state_matrix = state_matrix
        self.input_matrix = input_matrix
        self.output_matrix = output_matrix
        self.feedthrough_matrix = feedthrough_matrix

        self.current_state = initial_state
        self.current_time = initial_time

    def get_state_change(self, control_input: Vector, current_state: Vector = None):
        if current_state is None:
            current_state = self.current_state

        return self.state_matrix @ current_state + self.input_matrix @ control_input

    def get_output(self, control_input: Vector, current_state: Vector = None):
        if current_state is None:
            current_state = self.current_state

        return self.output_matrix @ current_state + self.feedthrough_matrix @ control_input

    def update(self, new_state: Vector, time_change: float):
        self.current_time += time_change
        self.current_state = new_state