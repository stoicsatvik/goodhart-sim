import unittest
from goodhart_sim import Candidate, Config, evaluate_distribution_shift, matched_population_selection, matched_seed_comparison, pressure_sweep, sealed_seed_failure_rate, select_by_proxy, simulate
from report_goodhart import build_report

class ScalarGoodhartContracts(unittest.TestCase):
    def test_zero_pressure_has_no_gaming(self):
        out=simulate(Config(0.0)); self.assertEqual((out.gaming,out.proxy,out.true_objective),(0.0,1.0,1.0))
    def test_high_pressure_improves_proxy_while_true_goal_worsens(self):
        low,high=simulate(Config(0.25)),simulate(Config(1.0)); self.assertGreater(high.proxy,low.proxy); self.assertLess(high.true_objective,low.true_objective)
    def test_same_config_is_deterministic(self): self.assertEqual(simulate(Config(0.75)),simulate(Config(0.75)))
    def test_sweep_preserves_order(self):
        p=(0.0,0.25,0.5,0.75,1.0); o=pressure_sweep(p); self.assertEqual(o[-1],simulate(Config(1.0)))
    def test_invalid_pressure_fails_closed(self):
        with self.assertRaises(ValueError): simulate(Config(1.01))
    def test_noise_requires_seed(self):
        with self.assertRaises(ValueError): simulate(Config(0.5,measurement_noise=0.1))
    def test_seed_repeatability(self):
        c=Config(0.75,0.2,17); self.assertEqual(simulate(c),simulate(c))
    def test_distinct_seeds(self):
        a,b=simulate(Config(0.75,0.2,17)),simulate(Config(0.75,0.2,29)); self.assertNotEqual(a.measurement_error,b.measurement_error); self.assertEqual(a.true_objective,b.true_objective)
    def test_matched_seed(self):
        low,high=matched_seed_comparison(0.25,1.0,0.2,17); self.assertEqual(low.measurement_error,high.measurement_error); self.assertGreater(high.proxy,low.proxy); self.assertLess(high.true_objective,low.true_objective)
    def test_sealed_seeds(self): self.assertEqual(sealed_seed_failure_rate((3,11,17,29,41,53,71,89)),1.0)
    def test_empty_seeds_fail(self):
        with self.assertRaises(ValueError): sealed_seed_failure_rate(())

class SelectionEffectContracts(unittest.TestCase):
    def setUp(self): self.population=(Candidate(1.0,0.1),Candidate(0.8,1.0),Candidate(0.9,0.35))
    def test_pressure_changes_selection(self):
        low,high=matched_population_selection(self.population,0.25,1.0,1); self.assertEqual(low.selected_indices,(0,)); self.assertEqual(high.selected_indices,(1,)); self.assertGreater(high.mean_proxy,low.mean_proxy); self.assertLess(high.mean_true_objective,low.mean_true_objective)
    def test_deterministic(self): self.assertEqual(select_by_proxy(self.population,0.75,2),select_by_proxy(self.population,0.75,2))
    def test_ties(self): self.assertEqual(select_by_proxy((Candidate(1,0),Candidate(1,0)),0.5,1).selected_indices,(0,))
    def test_invalid_size(self):
        with self.assertRaises(ValueError): select_by_proxy(self.population,0.5,0)
    def test_empty(self):
        with self.assertRaises(ValueError): select_by_proxy((),0.5,1)

class DistributionShiftContracts(unittest.TestCase):
    def setUp(self):
        self.train=(Candidate(1.0,0.1),Candidate(0.85,0.4),Candidate(0.8,0.8))
        self.shifted=(Candidate(0.7,0.1),Candidate(0.75,0.4),Candidate(0.72,1.3))
    def test_no_shift_control_is_exactly_zero(self):
        r=evaluate_distribution_shift(self.train,self.train,1.0,1); self.assertEqual(r.proxy_delta,0.0); self.assertEqual(r.true_objective_delta,0.0); self.assertEqual(r.train,r.evaluation)
    def test_shift_can_preserve_proxy_appeal_while_degrading_goal(self):
        r=evaluate_distribution_shift(self.train,self.shifted,1.0,1); self.assertGreaterEqual(r.evaluation.mean_proxy,r.train.mean_proxy); self.assertLess(r.evaluation.mean_true_objective,r.train.mean_true_objective)
    def test_shift_is_exactly_repeatable(self): self.assertEqual(evaluate_distribution_shift(self.train,self.shifted,1.0,1),evaluate_distribution_shift(self.train,self.shifted,1.0,1))
    def test_unequal_population_sizes_fail_closed(self):
        with self.assertRaises(ValueError): evaluate_distribution_shift(self.train,self.shifted[:-1],1.0,1)
    def test_empty_shift_fails_closed(self):
        with self.assertRaises(ValueError): evaluate_distribution_shift((),(),1.0,1)

class ReportContracts(unittest.TestCase):
    def test_default_report_exposes_failure_and_claim_boundary(self):
        report=build_report(0.25,1.0)
        self.assertIn("proxy_delta=+",report)
        self.assertIn("true_objective_delta=-",report)
        self.assertIn("goodhart_failure=YES",report)
        self.assertIn("claim_boundary=synthetic fixture",report)
    def test_report_is_exactly_repeatable(self): self.assertEqual(build_report(0.25,1.0),build_report(0.25,1.0))
    def test_single_pressure_change_can_remove_failure(self): self.assertIn("goodhart_failure=NO",build_report(0.25,0.25))

if __name__=='__main__': unittest.main()
