from typing import Callable

import numpy as np
from matplotlib import pyplot as plt
from numpy.f2py.auxfuncs import throw_error

from Utilities.types import Vector, Matrix
from Utilities.utils import rk4, euler
from classes.Signals import Signal
from classes.StateSpaceSystem import StateSpaceSystem


class SystemSimulation:
    def __init__(self, step_size, simulated_system: StateSpaceSystem, rk4_method: bool = True, euler_method: bool = False, tolerance: float = 1e-5, current_time: float = 0):
        self.current_time = current_time
        self.step_size = step_size
        self.system = simulated_system
        self.history = {"time": [], "state": [], "output": []}
        self.euler_method = euler_method
        self.rk4_method = rk4_method
        self.tolerance = tolerance

    # Runtime
    def _calc_step(self, state: Vector, control_input: Vector, step_size: float):
        if self.rk4_method and not self.euler_method:
            return rk4(self.system.get_state_change, state, control_input, step_size)
        elif self.euler_method and not self.rk4_method:
            return euler(self.system.get_state_change, state, control_input, step_size)
        else:
            raise ValueError("No method chosen")

    def step(self, control_input: Signal):


        control_input = np.array(control_input)
        self.system.check_input_size(control_input)
        control_input_final = control_input.copy()
        for row in range(len(control_input)):
            control_input_final[row][0] = self.input_validator(control_input[row][0])

        output = self.system.get_output(control_input_final)

        self.history["time"].append(self.current_time)
        self.history["state"].append(self.system.current_state.copy())
        self.history["output"].append(output.copy())

        value_confirmed = False
        current_step = 0
        while not value_confirmed:
            full_step = self._calc_step(self.system.current_state, control_input_final, self.step_size)
            half_input = np.array([[row[0](self.current_time + self.step_size / 2)] for row in control_input])

            half_1 = self._calc_step(self.system.current_state, control_input_final, self.step_size / 2)
            half_2 = self._calc_step(half_1, half_input, self.step_size / 2)

            error = np.max(np.abs(full_step - half_2))

            if error <= self.tolerance:
                value_confirmed = True
                current_step = half_2
                self.current_time += self.step_size

                if error < self.tolerance / 10 and error:
                    self.step_size = min(self.step_size * 1.2, 0.02)
            else:
                self.step_size /= 2

        self.history["time"].append(self.current_time)
        self.history["state"].append(self.system.current_state.copy())
        self.history["output"].append(output.copy())

        self.system.update(current_step)

    def run(self, control_input: Matrix, simulation_time: float):
        while self.current_time < simulation_time:
            self.step(control_input)
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

    def input_validator(self, control_input):
        if callable(control_input):
            control_input = control_input(self.current_time)

        return control_input

    def __str__(self):
        lines = []
        i = 0
        for t, s, o in zip(self.history["time"], self.history["state"], self.history["output"]):
            if i == 0:
                lines.append(f"Time: {t:.2f}s | State: {s.flatten()} | Output: {o.flatten()}")
            i += 1
            i = i % 50

        return "\n".join(lines)

    def plot_results(self):
        """Rysuje wykres wyjścia (output) w czasie."""
        if not self.history["time"]:
            print("Brak danych do narysowania. Uruchom najpierw symulację.")
            return

        plt.figure(figsize=(10, 5))

        # Zamieniamy listę wektorów w jedną macierz i usuwamy puste wymiary
        y = np.array(self.history["output"]).squeeze()
        time_axis = self.history["time"]

        # Jeśli układ ma wiele wyjść (macierz C ma więcej niż jeden wiersz),
        # y będzie dwuwymiarowe. Rysujemy wtedy każde wyjście osobną linią.
        if y.ndim > 1:
            for i in range(y.shape[1]):
                plt.plot(time_axis, y[:, i], label=f'Wyjście {i}')
        else:
            # Dla pojedynczego wyjścia
            plt.plot(time_axis, y, label='Wyjście')

        plt.title("Symulacja układu")
        plt.xlabel("Czas [s]")
        plt.ylabel("Amplituda")
        plt.grid(True)
        plt.legend()
        plt.show()
