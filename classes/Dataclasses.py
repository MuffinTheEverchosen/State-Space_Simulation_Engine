from dataclasses import dataclass, field

from classes.StateSpaceSystem import StateSpaceSystem


@dataclass
class SystemHistory:
    state: list = field(default_factory=list)
    output: list = field(default_factory=list)

@dataclass
class SimulationData:
    time: list = field(default_factory=list)
    indexes: dict[StateSpaceSystem, int] = field(default_factory=dict)
    systems: dict[int, SystemHistory] = field(default_factory=dict)