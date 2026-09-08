import unittest
from goodhart_sim import Config, pressure_sweep, simulate


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

    def test_v0_rejects_unmodelled_noise_instead_of_faking_randomness(self):
        with self.assertRaises(ValueError):
            simulate(Config(0.5, measurement_noise=0.1))


if __name__ == "__main__":
    unittest.main()
