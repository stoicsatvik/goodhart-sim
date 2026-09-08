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
- Exact challenger commit: `791bf57d7367786f42d66a261a473baac0ff407a`.
- Evidence: GitHub Actions workflow run `34205329030` completed successfully on the exact challenger head.
- Capability: same declared synthetic population at low and high optimization pressure; proxy ranking with latent outcomes preserved separately; deterministic index tie-breaking.
- Executed contracts require pressure to change the selected candidate in the declared fixture while increasing selected mean proxy and decreasing selected mean latent objective; deterministic repetition, tie handling, empty-population rejection, and invalid selection-size rejection also pass.
- Promotion status: SUPPORTED on the committed synthetic contracts.

## Claim boundary
This is a synthetic educational model, not evidence that any real organization or KPI follows these equations. Scalar gaming, seeded measurement noise, and the declared selection-effect fixture are SUPPORTED only on committed synthetic contracts. Distribution shift and real-world external validity remain NOT YET PROVEN.

## Highest-EV next move
Keep `791bf57d...` frozen as the selection-effect champion. Add a minimal deterministic distribution-shift challenger using matched configuration budgets and explicit train/evaluation populations. Promotion must show whether a proxy policy that looks acceptable on one declared population degrades under a shifted population, include a no-shift control, deterministic repeatability, and fail-closed invalid shift definitions. Do not infer real-world distribution shift from the synthetic result.

Status: ACTIVE / SCALAR + SEEDED-NOISE + SELECTION EFFECTS SUPPORTED / DISTRIBUTION-SHIFT CHALLENGER NEXT
