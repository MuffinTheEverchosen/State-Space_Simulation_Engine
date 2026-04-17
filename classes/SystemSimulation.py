from typing import Callable

import numpy as np
from matplotlib import pyplot as plt

from Utilities.types import Vector, Matrix
from Utilities.utils import rk4
from classes.Dataclasses import SimulationData, SystemHistory
from classes.StateSpaceSystem import StateSpaceSystem

class SystemSimulation:
    def __init__(self, step_size, simulated_system: StateSpaceSystem, current_time: float = 0):
        self.current_time = current_time
        self.step_size = step_size
        self.system = simulated_system
        self.history = {"time": [], "state": [], "output": []}

    # Runtime

    def step(self, control_input: Vector):
        self.system.check_input_size(control_input)
        output = self.system.get_output(control_input)
        rk4_step = rk4(self.system.get_state_change, self.system.current_state, control_input, self.step_size)

        self.history["time"].append(self.current_time)
        self.history["state"].append(self.system.current_state.copy())
        self.history["output"].append(output.copy())

        self.system.update(rk4_step)

        self.current_time += self.step_size

    def run(self, control_input: Matrix, simulation_time: float):
        while self.current_time < simulation_time:
            self.step(control_input)

    def rewind(self, number_of_steps_back: int):
        state_to_rewind = self.history["state"][len(self.history["time"]) - number_of_steps_back - 1]
        self.system.current_state = state_to_rewind
        self.current_time -= number_of_steps_back * self.step_size

        for steps in range(number_of_steps_back):
            self.history["time"].pop()
            self.history["state"].pop()
            self.history["output"].pop()

    def reset(self):
        self.system.current_state = self.history["state"][0]
        self.current_time = self.history["time"][0]

        self.history["time"] = []
        self.history["state"] = []
        self.history["output"] = []

    # getters

    def get_state(self, time):
        for t, s, o in zip(self.history["time"], self.history["state"]):
            if t == time:
                return s
        raise ValueError("Wrong time")

    def get_output(self, time):
        for t, o in zip(self.history["time"], self.history["output"]):
            if t == time:
                return o
        raise ValueError("Wrong time")

    def __str__(self):
        lines = []

        for t, s, o in zip(self.history["time"], self.history["state"], self.history["output"]):
            lines.append(f"Time: {t:.2f}s | State: {s.flatten()} | Output: {o.flatten()}")

        return "\n".join(lines)