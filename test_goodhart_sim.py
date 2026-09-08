import unittest
from goodhart_sim import (
    Config,
    matched_seed_comparison,
    pressure_sweep,
    sealed_seed_failure_rate,
    simulate,
)


class ScalarGoodhartContracts(unittest.TestCase):
    def test_zero_pressure_has_no_gaming(self):
        out = simulate(Config(0.0))
        self.assertEqual(out.gaming, 0.0)
        self.assertEqual(out.proxy, 1.0)
        self.assertEqual(out.true_objective, 1.0)

    def test_high_pressure_improves_proxy_while_true_goal_worsens(self):
        low = simulate(Config(0.25))
        high = simulate(Config(1.0))
        self.assertGreater(high.proxy, low.proxy)
        self.assertLess(high.true_objective, low.true_objective)

    def test_same_config_is_byte_for_byte_deterministic(self):
        self.assertEqual(simulate(Config(0.75)), simulate(Config(0.75)))

    def test_sweep_preserves_declared_order(self):
        pressures = (0.0, 0.25, 0.5, 0.75, 1.0)
        outcomes = pressure_sweep(pressures)
        self.assertEqual(len(outcomes), len(pressures))
        self.assertEqual(outcomes[-1], simulate(Config(1.0)))

    def test_invalid_pressure_fails_closed(self):
        with self.assertRaises(ValueError):
            simulate(Config(1.01))

    def test_noise_requires_explicit_seed(self):
        with self.assertRaises(ValueError):
            simulate(Config(0.5, measurement_noise=0.1))

    def test_identical_seed_is_exactly_repeatable(self):
        config = Config(0.75, measurement_noise=0.2, noise_seed=17)
        self.assertEqual(simulate(config), simulate(config))

    def test_declared_seeds_produce_distinct_measurement_errors(self):
        a = simulate(Config(0.75, measurement_noise=0.2, noise_seed=17))
        b = simulate(Config(0.75, measurement_noise=0.2, noise_seed=29))
        self.assertNotEqual(a.measurement_error, b.measurement_error)
        self.assertEqual(a.true_objective, b.true_objective)

    def test_matched_seed_cancels_observation_error_between_pressures(self):
        low, high = matched_seed_comparison(0.25, 1.0, 0.2, 17)
        self.assertEqual(low.measurement_error, high.measurement_error)
        self.assertGreater(high.proxy, low.proxy)
        self.assertLess(high.true_objective, low.true_objective)

    def test_goodhart_failure_survives_fixed_sealed_seed_set(self):
        sealed = (3, 11, 17, 29, 41, 53, 71, 89)
        self.assertEqual(sealed_seed_failure_rate(sealed), 1.0)

    def test_empty_sealed_seed_set_fails_closed(self):
        with self.assertRaises(ValueError):
            sealed_seed_failure_rate(())


if __name__ == "__main__":
    unittest.main()
