#!/usr/bin/env python 

import unittest as ut
from startrader import model as m


class StarsNaming(ut.TestCase):

    @ut.skip("Trying to understand")
    def test_naming_one_star(self):
        game = m.Game()
        game.stars.append(m.Star("", None, None, None, 1, 1, 2, 1, 2070))


class CoordinateTests(ut.TestCase):

    def test_initial_number_of_stars(self):
        game = m.Game()
        self.assertEqual(2, len(game.fleets))
        self.assertEqual(7, len(game.stars))
