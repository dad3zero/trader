#!/usr/bin/env python 

import unittest as ut
from startrader import model as m


class BasicBehavior(ut.TestCase):

    def test_something(self):
        self.assertEqual("COSMOPOLITAN", m.EvolutionLevel.COSMOPOLITAN.name)