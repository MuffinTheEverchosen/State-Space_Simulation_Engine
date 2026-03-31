from typing import Callable

import numpy as np
import numpy.typing as npt
from Utilities.types import Vector


def rk4(state_change: Callable, current_state: Vector, control_input: Vector, step_size: float):
    k1 = state_change(control_input, current_state)
    k2 = state_change(control_input, current_state + k1 * (step_size / 2))
    k3 = state_change(control_input, current_state + k2 * (step_size / 2))
    k4 = state_change(control_input, current_state + k3 * step_size)

    weighted_slope = ( k1 + 2 * k2 + 2 * k3 + k4 ) / 6

    return current_state + weighted_slope * step_size

def check_matrix_dimensions(matrix: np.ndarray, desired_amount):
    if matrix.ndim != desired_amount:
        raise ValueError("Wrong matrix dimensions")
