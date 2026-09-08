"""Dependency-free CLI report for the validated scalar Goodhart fixture."""
import argparse
from goodhart_sim import Config, simulate


def build_report(low_pressure: float, high_pressure: float) -> str:
    low = simulate(Config(low_pressure))
    high = simulate(Config(high_pressure))
    proxy_delta = high.proxy - low.proxy
    objective_delta = high.true_objective - low.true_objective
    failure = proxy_delta > 0.0 and objective_delta < 0.0
    return "\n".join((
        "Goodhart Sim V0 synthetic report",
        f"low_pressure={low_pressure:.3f} proxy={low.proxy:.6f} true_objective={low.true_objective:.6f}",
        f"high_pressure={high_pressure:.3f} proxy={high.proxy:.6f} true_objective={high.true_objective:.6f}",
        f"proxy_delta={proxy_delta:+.6f}",
        f"true_objective_delta={objective_delta:+.6f}",
        f"goodhart_failure={'YES' if failure else 'NO'}",
        "claim_boundary=synthetic fixture; no real-world external-validity claim",
    ))


def main() -> None:
    parser = argparse.ArgumentParser(description="Reproduce the V0 scalar Goodhart report.")
    parser.add_argument("--low-pressure", type=float, default=0.25)
    parser.add_argument("--high-pressure", type=float, default=1.0)
    args = parser.parse_args()
    print(build_report(args.low_pressure, args.high_pressure))


if __name__ == "__main__":
    main()
