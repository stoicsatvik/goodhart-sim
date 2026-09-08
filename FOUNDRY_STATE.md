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

## Frozen scalar champion
- Branch: `foundry/v0-scalar-sim`; do not merge without explicit approval.
- Champion commit: `799a4f4b73397479dfb5c12cb6f08864f4ab6049`.
- Evidence: GitHub Actions workflow run `34190851578`, job `core-contracts` (`101948435135`), completed successfully on Python 3.12.
- `goodhart_sim.py`: deterministic scalar environment separating productive effort, gaming, observable proxy, and latent true objective.
- `test_goodhart_sim.py`: six contracts covering zero-pressure behavior, proxy/goal divergence, determinism, ordered sweeps, invalid pressure, and rejection of unmodelled noise.
- Runtime evidence: SUPPORTED for the committed deterministic synthetic contracts.

## Claim boundary
This is a synthetic educational model, not evidence that any real organization or KPI follows these equations. Measurement noise, selection effects, and distribution shift are NOT YET PROVEN / unimplemented. A green deterministic scalar gate does not establish those extensions or external validity.

## Highest-EV next move
Keep `799a4f4b...` frozen as champion. Add a challenger with deterministic seeded measurement noise and matched-seed pressure comparisons. Require exact repeatability for identical seeds, divergence across at least two declared seeds, and preservation/detection of the Goodhart failure under a fixed sealed seed set before promotion. Do not use unseeded randomness.

Status: ACTIVE / SCALAR CHAMPION SUPPORTED / SEEDED-NOISE CHALLENGER NEXT
