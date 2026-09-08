# Foundry State

## Objective
Build reproducible simulations showing how useful metrics degrade when agents are rewarded for optimizing the proxy rather than the underlying goal.

## Public boundary
Keep this educational and generic. Do not encode private organizational metrics, proprietary strategy models, or sensitive behavioral data.

## V0 milestone
- Simple principal/agent environment with latent true objective and observable proxy
- Configurable optimization pressure and measurement noise
- Plot/report proxy improvement versus true-outcome degradation
- Multiple failure modes: gaming, selection effects, distribution shift
- Deterministic seeds and tests

## Acceptance
A user can change one config value for optimization pressure and reproduce a clear case where the measured KPI improves while the real objective worsens.

## Current challenger
- Branch: `foundry/v0-scalar-sim`; do not merge without explicit approval.
- `goodhart_sim.py`: deterministic scalar environment separating productive effort, gaming, observable proxy, and latent true objective.
- `test_goodhart_sim.py`: contracts for zero-pressure behavior, proxy/goal divergence, determinism, ordered sweeps, invalid pressure, and explicit rejection of unmodelled noise.
- Architecture/committed contracts: SUPPORTED as inspectable code.
- Runtime evidence: NOT YET PROVEN until the exact branch head executes the contracts in a reproducible environment.

## Claim boundary
This is a synthetic educational model, not evidence that any real organization or KPI follows these equations. Measurement noise, selection effects, and distribution shift are not yet implemented.

## Highest-EV next move
Execute `python -m unittest -v` on the exact branch head. If green, freeze the scalar gaming case as the first champion and add deterministic measurement noise with fixed seeds; if red, preserve the counterexample and repair semantics before expansion.

Status: ACTIVE / SCALAR CHALLENGER NOT YET PROVEN
