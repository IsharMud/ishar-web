"""The essence tables from ishar-mud#1990 / #2004. Plain unittest, no
database: ``python -m unittest apps.fated.tests``."""
from unittest import TestCase

from .essence import SeasonEssence, bank, loose_value, season_total


class BankTest(TestCase):
    def test_bank_by_tension(self):
        table = {0: 16, 1: 19, 2: 22, 3: 25, 4: 28, 5: 32, 6: 35, 7: 38,
                 8: 41, 9: 44, 10: 48, 19: 76, 23: 89}
        for tension, expected in table.items():
            with self.subTest(tension=tension):
                self.assertEqual(bank(tension), expected)

    def test_ascension_adds_six_multipliers_over_the_summit(self):
        self.assertEqual(bank(0) - loose_value(10, 0), 6)
        self.assertEqual(bank(5) - loose_value(10, 5), 12)


class LooseTest(TestCase):
    def test_loose_by_remorts_and_tension(self):
        table = {(1, 5): 2, (5, 5): 10, (10, 5): 20, (8, 8): 20,
                 (1, 19): 4, (5, 19): 24, (10, 19): 48}
        for (remorts, tension), expected in table.items():
            with self.subTest(remorts=remorts, tension=tension):
                self.assertEqual(loose_value(remorts, tension), expected)

    def test_remorts_clamp_to_the_summit(self):
        self.assertEqual(loose_value(-3, 5), 0)
        self.assertEqual(loose_value(14, 5), loose_value(10, 5))

    def test_untied_tension_reckons_as_zero(self):
        self.assertEqual(loose_value(4, -1), 4)


class SeasonTotalTest(TestCase):
    def test_bonuses(self):
        self.assertEqual(season_total(0, 0, played=False, milestones=0), 0)
        self.assertEqual(season_total(0, 0, played=True, milestones=3), 5)
        self.assertEqual(season_total(16, 0, played=False, milestones=0), 19)


class RealCaseTest(TestCase):
    """Woven 0, loose 21 set under the earlier rule, 6 milestones, the
    living character at remort 1, Tension 19."""

    def setUp(self):
        self.essence = SeasonEssence(
            woven=0, loose=21, loose_remorts=0, loose_tension=0, played=True,
            milestones=6, life_remorts=1, life_tension=19,
        )

    def test_total(self):
        self.assertEqual(self.essence.total, 30)

    def test_loose_has_no_recorded_source(self):
        self.assertTrue(self.essence.earlier_rule)

    def test_this_life_stands_below_the_high_water(self):
        self.assertEqual(self.essence.life_worth, 4)
        self.assertTrue(self.essence.below_high_water)

    def test_passes_the_high_water_at_remort_five(self):
        step = self.essence.passes_at
        self.assertEqual((step.remorts, step.worth), (5, 24))
        self.assertEqual(sum(s.passes for s in self.essence.steps), 1)
        self.assertEqual(self.essence.steps[2].total, 30)   # remort 4: 19, holds
        self.assertEqual(step.total, 33)

    def test_ascension(self):
        ascension = self.essence.ascension
        self.assertEqual(ascension.bank, 76)
        self.assertEqual(ascension.loose_replaced, 48)
        self.assertEqual((ascension.total_before, ascension.total_after), (57, 85))
        self.assertEqual(ascension.change, 28)
        self.assertEqual(ascension.change_display, "+28")

    def test_multiplier(self):
        self.assertEqual(self.essence.multiplier_display, "\u00d74.8")


class LowerTensionAscensionTest(TestCase):
    def test_weaving_in_below_an_earlier_high_water_lowers_the_total(self):
        essence = SeasonEssence(
            woven=0, loose=48, loose_remorts=10, loose_tension=19, played=True,
            milestones=0, life_remorts=2, life_tension=0,
        )
        self.assertIsNone(essence.passes_at)
        self.assertEqual(essence.ascension.bank, 16)
        self.assertEqual(essence.ascension.change, -32)
        self.assertEqual(essence.ascension.change_display, "\u221232")
        self.assertEqual(essence.multiplier_display, "\u00d71")


class NoLifeTest(TestCase):
    def test_no_life_means_no_projection(self):
        essence = SeasonEssence(
            woven=32, loose=0, loose_remorts=0, loose_tension=0, played=True,
            milestones=2,
        )
        self.assertEqual(essence.total, 37)
        self.assertEqual(essence.steps, [])
        self.assertIsNone(essence.ascension)
        self.assertFalse(essence.earlier_rule)
