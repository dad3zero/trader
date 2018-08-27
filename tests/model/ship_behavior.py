#!/usr/bin/env python 

import unittest as ut
from startrader import model as m


class ShipLocation(ut.TestCase):

    def test_start_location_none(self):
        ship = m.Ship(None)
        self.assertIsNone(ship.star)

    def test_can_set_location(self):
        ship = m.Ship(None)
        ship.location = "here"
        self.assertEqual("here", ship.star)
        self.assertEqual("here", ship.location)
