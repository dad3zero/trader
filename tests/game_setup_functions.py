#!/usr/bin/env python 

import unittest as ut
from startrader import trader as t
from startrader import model as m


class StarsNaming(ut.TestCase):

    @ut.skip("Trying to understand")
    def test_naming_one_star(self):
        game = m.Game()
        game.stars.append(m.Star(None, None, None, 1, 1, 2, 1, 2070, ""))
        t.name_star(game, 0)


class CoordinateTests(ut.TestCase):

    def test_false_coordinates(self):
        game = m.Game()
        game.stars.append(m.Star(None, None, None, 1, 1, 2, 1, 2070, ""))
        result = t.good_coords(game, 1, -1, -1)
        self.assertEqual(2, game.half)
        self.assertFalse(result)
