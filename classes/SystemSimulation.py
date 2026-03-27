from Utilities.types import Vector
from Utilities.utils import rk4
from classes.StateSpaceSystem import StateSpaceSystem


class SystemSimulation:
    def __init__(self, step_size: float, current_time: float = 0):
        self.step_size = step_size
        self.current_time = current_time

        self.history = {"time": [], "state": [], "output": []}

    def step(self, system: StateSpaceSystem, control_input: Vector):
        output = system.get_output(control_input)
        rk4_step = rk4(system.get_state_change, system.current_state, control_input, self.step_size)

        self.history["time"].append(self.current_time)
        self.history["state"].append(system.current_state.copy())
        self.history["output"].append(output.copy())

        system.update(rk4_step, self.step_size)

        self.current_time += self.step_size

    def __str__(self):
        lines = []

        for t, s, o in zip(self.history["time"], self.history["state"], self.history["output"]):
            lines.append(f"Time: {t:.2f}s | State: {s.flatten()} | Output: {o.flatten()}")

        return "\n".join(lines)