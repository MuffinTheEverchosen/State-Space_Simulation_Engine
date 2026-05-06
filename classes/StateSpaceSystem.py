import numpy as np

from Utilities.types import Matrix, Vector
from Utilities.utils import check_matrix_dimensions


class StateSpaceSystem:
    def __init__(self, state_matrix: Matrix, input_matrix: Matrix, output_matrix: Matrix, initial_state: Vector, feedthrough_matrix: Matrix = None):
        state_matrix = np.array(state_matrix, dtype=float)
        input_matrix = np.array(input_matrix, dtype=float)
        output_matrix = np.array(output_matrix, dtype=float)
        initial_state = np.array(initial_state, dtype=float)

        check_matrix_dimensions(state_matrix, 2)
        check_matrix_dimensions(input_matrix, 2)
        check_matrix_dimensions(output_matrix, 2)
        check_matrix_dimensions(initial_state, 2)

        if feedthrough_matrix == None:
            feedthrough_matrix = np.zeros((output_matrix.shape[0], input_matrix.shape[1]))
        else:
            feedthrough_matrix = np.array(feedthrough_matrix, dtype=float)

        check_matrix_dimensions(feedthrough_matrix, 2)

        if state_matrix.shape[0] != state_matrix.shape[1] or state_matrix.shape[0] != output_matrix.shape[1]:
            raise ValueError("Wrong height/width of state_matrix or height of output_matrix")
        elif input_matrix.shape[1] != feedthrough_matrix.shape[1]:
            raise ValueError("Wrong height of input_matrix or height of feedthrough_matrix")
        elif output_matrix.shape[0] != feedthrough_matrix.shape[0]:
            raise ValueError("Wrong width of output_matrix or width of feedthrough_matrix")
        elif initial_state.shape[0] != state_matrix.shape[0]:
            raise ValueError("Wrong width of initial_state matrix")

        self.state_matrix = state_matrix
        self.input_matrix = input_matrix
        self.output_matrix = output_matrix
        self.feedthrough_matrix = feedthrough_matrix

        self.current_state = initial_state

    def get_state_change(self, control_input: Vector, current_state: Vector) -> Matrix:
        return self.state_matrix @ current_state + self.input_matrix @ control_input

    def get_output(self, control_input: Vector) -> Matrix:
        return self.output_matrix @ self.current_state + self.feedthrough_matrix @ control_input

    def update(self, new_state: Vector):
        self.current_state = new_state

    def check_input_size(self, control_input: Vector):
        if self.input_matrix.shape[1] != control_input.shape[1]:
            raise ValueError("Wrong height of control_input")