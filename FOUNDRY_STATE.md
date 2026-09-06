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

## Next move
Implement the minimal scalar simulation and regression tests before adding dashboards or AI agents.

Status: ACTIVE / NOT YET PROVEN
