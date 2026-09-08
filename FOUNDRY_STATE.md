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
- Promotion status: SUPPORTED on the committed synthetic contracts.

## Selection-effect challenger
- Exact challenger commit: `791bf57d7367786f42d66a261a473baac0ff407a`.
- Evidence: GitHub Actions workflow run `34205329030` completed successfully on the exact challenger head.
- Capability: same declared synthetic population at low and high optimization pressure; proxy ranking with latent outcomes preserved separately; deterministic index tie-breaking.
- Promotion status: SUPPORTED on the committed synthetic contracts.

## Distribution-shift challenger
- Exact challenger commit: `595027393f3d22d47aded8c2798e65042b62c04d`.
- Evidence: GitHub Actions workflow run `34210259797` (`Foundry core contracts`) completed successfully on the exact challenger head.
- Capability: same proxy-selection rule, optimization pressure, and selection budget evaluated against explicit train/evaluation populations.
- Executed contracts include an exact-zero no-shift control, a declared shifted population where proxy appeal is preserved while the latent objective degrades, exact deterministic repetition, unequal-population rejection, and empty-population rejection.
- Promotion status: SUPPORTED on the committed synthetic contracts.

## Claim boundary
This is a synthetic educational model, not evidence that any real organization or KPI follows these equations. Scalar gaming, seeded measurement noise, selection effects, and the declared distribution-shift fixture are SUPPORTED only on committed synthetic contracts. Real-world external validity remains NOT YET PROVEN.

## Highest-EV next move
Freeze `595027393...` as the V0 synthetic failure-mode champion. The remaining V0 acceptance gap is a reproducible user-facing report/CLI that exposes proxy improvement versus latent-objective degradation without changing the validated mechanics. Keep reporting deterministic and dependency-light; do not add dashboards or AI wrappers before the minimal report contract is executable. After that gate, shift OSS allocation to `constraint-graph` / `decision-tree-lab` unless adoption evidence changes expected value.

Status: ACTIVE / V0 SYNTHETIC FAILURE MODES SUPPORTED / REPORT CONTRACT NEXT
