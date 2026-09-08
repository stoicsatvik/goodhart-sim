"""Synthetic Goodhart simulator with deterministic noise and selection effects.

The latent objective rewards productive effort and penalizes gaming. Observable
proxies can reward gaming and contain seeded measurement error. Selection routines
rank a declared synthetic population by proxy while separately preserving latent
outcomes, so proxy-driven selection can be falsified without claiming real-world
organizational validity.
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


@dataclass(frozen=True)
class Candidate:
    base_productivity: float
    gaming_affinity: float


@dataclass(frozen=True)
class SelectionResult:
    selected_indices: tuple[int, ...]
    mean_proxy: float
    mean_true_objective: float


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


def evaluate_candidate(candidate: Candidate, optimization_pressure: float) -> Outcome:
    """Evaluate a declared synthetic candidate without measurement noise."""
    if not 0.0 <= optimization_pressure <= 1.0:
        raise ValueError("optimization_pressure must be in [0, 1]")
    if candidate.base_productivity < 0.0 or candidate.gaming_affinity < 0.0:
        raise ValueError("candidate parameters must be non-negative")
    p = optimization_pressure
    productive = candidate.base_productivity * (1.0 - 0.2 * p)
    gaming = candidate.gaming_affinity * p * p
    proxy = productive + 0.75 * gaming
    true_objective = productive - gaming
    return Outcome(productive, gaming, proxy, true_objective)


def select_by_proxy(
    population: tuple[Candidate, ...],
    optimization_pressure: float,
    select_n: int,
) -> SelectionResult:
    """Select top-N by proxy with deterministic index tie-breaking."""
    if not population:
        raise ValueError("population must not be empty")
    if not 1 <= select_n <= len(population):
        raise ValueError("select_n must be between 1 and population size")
    evaluated = tuple(
        evaluate_candidate(candidate, optimization_pressure) for candidate in population
    )
    ranked = sorted(range(len(population)), key=lambda i: (-evaluated[i].proxy, i))
    chosen = tuple(ranked[:select_n])
    return SelectionResult(
        selected_indices=chosen,
        mean_proxy=sum(evaluated[i].proxy for i in chosen) / select_n,
        mean_true_objective=sum(evaluated[i].true_objective for i in chosen) / select_n,
    )


def matched_population_selection(
    population: tuple[Candidate, ...],
    low_pressure: float,
    high_pressure: float,
    select_n: int,
) -> tuple[SelectionResult, SelectionResult]:
    """Compare selection pressure on exactly the same declared population."""
    return (
        select_by_proxy(population, low_pressure, select_n),
        select_by_proxy(population, high_pressure, select_n),
    )
