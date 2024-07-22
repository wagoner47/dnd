import unittest

from scipy import stats

from ..src.dice import Die


class TestDie(unittest.TestCase):
    def setUp(self):
        self.dice_sides = [2, 3, 4, 6, 8, 10, 12, 20]
        self.dice = [Die(n_sides, 0) for n_sides in self.dice_sides]

    def test_uniformity(self):
        for n_sides, die in zip(self.dice_sides, self.dice):
            self.assertGreaterEqual(
                stats.chisquare([die() for _ in range(int(1e6))], ddof=1).statistic,
                0.9,
                f"Bad distribution for die with {n_sides} sides",
            )
