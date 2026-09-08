"""Synthetic Goodhart simulator with deterministic noise, selection, and shift.

All mechanics are educational synthetic fixtures. Observable proxies are kept
separate from latent objectives so failures can be falsified without implying
real-world organizational validity.
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


@dataclass(frozen=True)
class ShiftResult:
    train: SelectionResult
    evaluation: SelectionResult
    proxy_delta: float
    true_objective_delta: float


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
        measurement_error = random.Random(config.noise_seed).uniform(-config.measurement_noise, config.measurement_noise)
    return Outcome(productive, gaming, latent_proxy + measurement_error, productive - config.gaming_harm * gaming, measurement_error)


def pressure_sweep(pressures: tuple[float, ...]) -> tuple[Outcome, ...]:
    if not pressures:
        raise ValueError("pressures must not be empty")
    return tuple(simulate(Config(p)) for p in pressures)


def matched_seed_comparison(low_pressure: float, high_pressure: float, measurement_noise: float, seed: int) -> tuple[Outcome, Outcome]:
    return simulate(Config(low_pressure, measurement_noise, seed)), simulate(Config(high_pressure, measurement_noise, seed))


def sealed_seed_failure_rate(seeds: tuple[int, ...], *, low_pressure: float = 0.25, high_pressure: float = 1.0, measurement_noise: float = 0.2) -> float:
    if not seeds:
        raise ValueError("seeds must not be empty")
    failures = 0
    for seed in seeds:
        low, high = matched_seed_comparison(low_pressure, high_pressure, measurement_noise, seed)
        failures += high.proxy > low.proxy and high.true_objective < low.true_objective
    return failures / len(seeds)


def evaluate_candidate(candidate: Candidate, optimization_pressure: float) -> Outcome:
    if not 0.0 <= optimization_pressure <= 1.0:
        raise ValueError("optimization_pressure must be in [0, 1]")
    if candidate.base_productivity < 0.0 or candidate.gaming_affinity < 0.0:
        raise ValueError("candidate parameters must be non-negative")
    p = optimization_pressure
    productive = candidate.base_productivity * (1.0 - 0.2 * p)
    gaming = candidate.gaming_affinity * p * p
    return Outcome(productive, gaming, productive + 0.75 * gaming, productive - gaming)


def select_by_proxy(population: tuple[Candidate, ...], optimization_pressure: float, select_n: int) -> SelectionResult:
    if not population:
        raise ValueError("population must not be empty")
    if not 1 <= select_n <= len(population):
        raise ValueError("select_n must be between 1 and population size")
    evaluated = tuple(evaluate_candidate(c, optimization_pressure) for c in population)
    ranked = sorted(range(len(population)), key=lambda i: (-evaluated[i].proxy, i))
    chosen = tuple(ranked[:select_n])
    return SelectionResult(chosen, sum(evaluated[i].proxy for i in chosen) / select_n, sum(evaluated[i].true_objective for i in chosen) / select_n)


def matched_population_selection(population: tuple[Candidate, ...], low_pressure: float, high_pressure: float, select_n: int) -> tuple[SelectionResult, SelectionResult]:
    return select_by_proxy(population, low_pressure, select_n), select_by_proxy(population, high_pressure, select_n)


def evaluate_distribution_shift(train_population: tuple[Candidate, ...], evaluation_population: tuple[Candidate, ...], optimization_pressure: float, select_n: int) -> ShiftResult:
    """Evaluate the same proxy-selection rule and budget on train and evaluation populations."""
    if not train_population or not evaluation_population:
        raise ValueError("train and evaluation populations must not be empty")
    if len(train_population) != len(evaluation_population):
        raise ValueError("matched shift evaluation requires equal population sizes")
    train = select_by_proxy(train_population, optimization_pressure, select_n)
    evaluation = select_by_proxy(evaluation_population, optimization_pressure, select_n)
    return ShiftResult(train, evaluation, evaluation.mean_proxy - train.mean_proxy, evaluation.mean_true_objective - train.mean_true_objective)
