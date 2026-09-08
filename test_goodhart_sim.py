import unittest
from goodhart_sim import (
    Candidate,
    Config,
    matched_population_selection,
    matched_seed_comparison,
    pressure_sweep,
    sealed_seed_failure_rate,
    select_by_proxy,
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


class SelectionEffectContracts(unittest.TestCase):
    def setUp(self):
        self.population = (
            Candidate(base_productivity=1.0, gaming_affinity=0.1),
            Candidate(base_productivity=0.8, gaming_affinity=1.0),
            Candidate(base_productivity=0.9, gaming_affinity=0.35),
        )

    def test_pressure_changes_who_proxy_selection_prefers(self):
        low, high = matched_population_selection(self.population, 0.25, 1.0, 1)
        self.assertEqual(low.selected_indices, (0,))
        self.assertEqual(high.selected_indices, (1,))

    def test_selection_can_raise_proxy_while_lowering_latent_objective(self):
        low, high = matched_population_selection(self.population, 0.25, 1.0, 1)
        self.assertGreater(high.mean_proxy, low.mean_proxy)
        self.assertLess(high.mean_true_objective, low.mean_true_objective)

    def test_selection_is_exactly_deterministic(self):
        expected = select_by_proxy(self.population, 0.75, 2)
        self.assertEqual(expected, select_by_proxy(self.population, 0.75, 2))

    def test_proxy_ties_break_by_declared_population_order(self):
        tied = (Candidate(1.0, 0.0), Candidate(1.0, 0.0))
        self.assertEqual(select_by_proxy(tied, 0.5, 1).selected_indices, (0,))

    def test_invalid_selection_size_fails_closed(self):
        with self.assertRaises(ValueError):
            select_by_proxy(self.population, 0.5, 0)
        with self.assertRaises(ValueError):
            select_by_proxy(self.population, 0.5, 4)

    def test_empty_population_fails_closed(self):
        with self.assertRaises(ValueError):
            select_by_proxy((), 0.5, 1)


if __name__ == "__main__":
    unittest.main()
