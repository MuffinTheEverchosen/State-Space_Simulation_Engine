import numpy as np
from matplotlib import pyplot as plt

from Utilities.types import Vector, Matrix
from Utilities.utils import rk4
from classes.StateSpaceSystem import StateSpaceSystem


class SystemSimulation:
    def __init__(self, current_time: float = 0):
        self.current_time = current_time

        self.history = {"time": [], "state": [], "output": []}

    # Runtime

    def step(self, system: StateSpaceSystem, control_input: Vector, step_size):
        system.check_input_size(control_input)
        output = system.get_output(control_input)
        rk4_step = rk4(system.get_state_change, system.current_state, control_input, step_size)

        self.history["time"].append(self.current_time)
        self.history["state"].append(system.current_state.copy())
        self.history["output"].append(output.copy())

        system.update(rk4_step, step_size)

        self.current_time += step_size

    def run(self, system: StateSpaceSystem, control_input: Matrix, simulation_time: float, step_size: float = None):
        if not step_size:
            step_size = simulation_time / 1000

        while self.current_time < simulation_time:
            self.step(system, control_input, step_size)

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

    # Testing

    def plot_system(self):
        # Reshape wymusza układ: wiersze = kroki czasowe, kolumny = konkretne wyjścia
        outputs = np.array(self.history["output"]).reshape(len(self.history["time"]), -1)

        plt.figure(figsize=(10, 5))

        # Rysuje osobną linię dla każdej kolumny z outputs
        for i in range(outputs.shape[1]):
            plt.plot(self.history["time"], outputs[:, i], label=f'Wyjście {i + 1}')

        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.xlabel('Czas [s]')
        plt.ylabel('Amplituda')
        plt.title('Odpowiedź układu dynamicznego')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
