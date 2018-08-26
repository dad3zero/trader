#!/usr/bin/env python 

import unittest as ut
from startrader import trader as t
from startrader import model as m


class SetShipDate(ut.TestCase):

    def setUp(self):
        self.ship = m.Ship(None, day=1, year=2070)

    def tearDown(self):
        del self.ship

    def test_add_one_day_to_ship(self):
        t.ship_days(self.ship, 1)
        self.assertEqual(2, self.ship.day)

    def test_add_one_year_to_ship(self):
        t.ship_days(self.ship, 360)
        self.assertEqual(1, self.ship.day)
        self.assertEqual(2071, self.ship.year)

    def test_add_more_than_a_year(self):
        t.ship_days(self.ship, 375)
        self.assertEqual(16, self.ship.day)
        self.assertEqual(2071, self.ship.year)

    def test_add_more_than_two_year(self):
        t.ship_days(self.ship, 735)
        self.assertEqual(16, self.ship.day)
        self.assertEqual(2072, self.ship.year)
