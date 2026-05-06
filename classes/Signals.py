from abc import ABC

import numpy as np


class Signal(ABC):
    def __init__(self, amplitude: float):
        self.amplitude = amplitude
    def __call__(self, t: float) -> float:
        pass

class SquareSignal(Signal):
    def __init__(self, amplitude: float, frequency: float, duty_cycle: float = 0.5):
        if duty_cycle < 0 or duty_cycle > 1:
            raise ValueError("Duty cycle higher than 1 or lower than 0")

        super().__init__(amplitude)
        self.period = 1 / frequency
        self.duty_cycle = duty_cycle

    def __call__(self, t: float):
        phase = t % self.period
        if phase <= self.duty_cycle * self.period:
            return self.amplitude
        else:
            return -self.amplitude

class SineSignal(Signal):
    def __init__(self, amplitude: float, frequency: float, phase: float = 0.0):
        super().__init__(amplitude)
        self.frequency = frequency
        self.phase = phase

    def __call__(self, t: float):
        return self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)

#class TriangleSignal(Signal):
