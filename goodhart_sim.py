"""Scalar Goodhart simulator with deterministic seeded measurement noise.

The latent objective rewards productive effort and penalizes gaming. The observable
proxy rewards both and may additionally contain seeded measurement error. Noise is
kept separate from the latent objective so matched-seed pressure comparisons do not
confound the underlying synthetic mechanism with observation error.
"""
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Config:
    optimization_pressure: float
    measurement_noise: float = 0.0
    noise_seed: int | None = None
    gaming_cost: float = 0.25
    gaming_harm: float = 1.0


@dataclass(frozen=True)
class Outcome:
    productive_effort: float
    gaming: float
    proxy: float
    true_objective: float
    measurement_error: float = 0.0


def simulate(config: Config) -> Outcome:
    if not 0.0 <= config.optimization_pressure <= 1.0:
        raise ValueError("optimization_pressure must be in [0, 1]")
    if config.measurement_noise < 0.0:
        raise ValueError("measurement_noise must be non-negative")
    if config.measurement_noise > 0.0 and config.noise_seed is None:
        raise ValueError("non-zero measurement_noise requires an explicit noise_seed")
    if config.gaming_cost < 0 or config.gaming_harm < 0:
        raise ValueError("cost/harm must be non-negative")

    p = config.optimization_pressure
    productive = 1.0 - 0.4 * p
    gaming = p * p
    latent_proxy = productive + gaming - config.gaming_cost * gaming
    measurement_error = 0.0
    if config.measurement_noise > 0.0:
        measurement_error = random.Random(config.noise_seed).uniform(
            -config.measurement_noise, config.measurement_noise
        )
    proxy = latent_proxy + measurement_error
    true_objective = productive - config.gaming_harm * gaming
    return Outcome(productive, gaming, proxy, true_objective, measurement_error)


def pressure_sweep(pressures: tuple[float, ...]) -> tuple[Outcome, ...]:
    if not pressures:
        raise ValueError("pressures must not be empty")
    return tuple(simulate(Config(p)) for p in pressures)


def matched_seed_comparison(
    low_pressure: float,
    high_pressure: float,
    measurement_noise: float,
    seed: int,
) -> tuple[Outcome, Outcome]:
    """Compare two pressure levels under exactly the same observation error draw."""
    low = simulate(Config(low_pressure, measurement_noise, seed))
    high = simulate(Config(high_pressure, measurement_noise, seed))
    return low, high


def sealed_seed_failure_rate(
    seeds: tuple[int, ...],
    *,
    low_pressure: float = 0.25,
    high_pressure: float = 1.0,
    measurement_noise: float = 0.2,
) -> float:
    """Fraction of declared seeds preserving proxy-up / true-objective-down divergence."""
    if not seeds:
        raise ValueError("seeds must not be empty")
    failures = 0
    for seed in seeds:
        low, high = matched_seed_comparison(
            low_pressure, high_pressure, measurement_noise, seed
        )
        failures += high.proxy > low.proxy and high.true_objective < low.true_objective
    return failures / len(seeds)
