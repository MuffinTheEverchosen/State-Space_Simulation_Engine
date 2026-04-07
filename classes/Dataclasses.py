from dataclasses import dataclass, field


@dataclass
class SystemHistory:
    state: list = field(default_factory=list)
    output: list = field(default_factory=list)

@dataclass
class SimulationData:
    time: list = field(default_factory=list)

    systems: dict[int, SystemHistory] = field(default_factory=dict)