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
- Runtime evidence: SUPPORTED for the committed deterministic synthetic contracts.

## Seeded-noise challenger
- Challenger commit: `47c087899d979fa6b8b30cdf94544b6adf13882a`.
- Evidence: GitHub Actions workflow run `34199582629` completed successfully.
- Capability: deterministic seeded measurement noise, matched-seed pressure comparisons, and a fixed sealed seed failure-rate gate.
- Promotion status: SUPPORTED on the committed synthetic contracts. Matching a seed preserves the same observation error across pressure conditions; distinct declared seeds produce distinct errors; the fixed sealed seed set preserves the proxy-up / true-objective-down failure.

## Selection-effect challenger
- Uses the same declared synthetic population at low and high optimization pressure.
- Ranks by observable proxy, preserves latent true-objective outcomes separately, and uses deterministic index tie-breaking.
- Promotion gate: low/high pressure must change the selected candidate in the declared fixture while increasing selected mean proxy and decreasing selected mean latent objective; exact repetition and invalid-input failure contracts must pass in CI.
- Runtime status: NOT YET PROVEN until the exact challenger head completes CI.

## Claim boundary
This is a synthetic educational model, not evidence that any real organization or KPI follows these equations. Scalar gaming and seeded measurement-noise mechanics are SUPPORTED only on committed synthetic contracts. Selection effects are NOT YET PROVEN pending exact-head CI. Distribution shift and real-world external validity remain NOT YET PROVEN.

## Highest-EV next move
Execute the selection-effect challenger through the existing narrow CI gate. If green, freeze its exact head and advance to a minimal deterministic distribution-shift falsification that preserves matched populations/configuration budgets. If red, preserve the failure and repair only the violated contract.

Status: ACTIVE / SCALAR + SEEDED-NOISE SUPPORTED / SELECTION CHALLENGER PENDING
