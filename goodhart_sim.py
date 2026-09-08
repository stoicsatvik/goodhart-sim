"""Deterministic scalar Goodhart simulator.

Architecture only until tests/CI execute. The latent objective rewards productive effort
and penalizes gaming; the observable proxy rewards both, so sufficient optimization
pressure can improve the proxy while degrading the true objective.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    optimization_pressure: float
    measurement_noise: float = 0.0
    gaming_cost: float = 0.25
    gaming_harm: float = 1.0


@dataclass(frozen=True)
class Outcome:
    productive_effort: float
    gaming: float
    proxy: float
    true_objective: float


def simulate(config: Config) -> Outcome:
    if not 0.0 <= config.optimization_pressure <= 1.0:
        raise ValueError("optimization_pressure must be in [0, 1]")
    if config.measurement_noise != 0.0:
        raise ValueError("v0 is deterministic; measurement_noise must be 0")
    if config.gaming_cost < 0 or config.gaming_harm < 0:
        raise ValueError("cost/harm must be non-negative")

    p = config.optimization_pressure
    productive = 1.0 - 0.4 * p
    gaming = p * p
    proxy = productive + gaming - config.gaming_cost * gaming
    true_objective = productive - config.gaming_harm * gaming
    return Outcome(productive, gaming, proxy, true_objective)


def pressure_sweep(pressures: tuple[float, ...]) -> tuple[Outcome, ...]:
    if not pressures:
        raise ValueError("pressures must not be empty")
    return tuple(simulate(Config(p)) for p in pressures)
