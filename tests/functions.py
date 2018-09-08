import unittest as ut
from startrader import trader
from startrader import model


class TestGetEarliestShip(ut.TestCase):
    def test_two_distint_ships_per_year(self):
        ships = [model.Ship(None, day=1, year=2070),
                 model.Ship(None, day=1, year=2080)]

        self.assertEqual(2070, trader.get_earliest_ship(ships).year)

    def test_two_distint_ships_per_day(self):
        ships = [model.Ship(None, day=21, year=2070),
                 model.Ship(None, day=20, year=2070)]

        self.assertEqual(20, trader.get_earliest_ship(ships).day)

    def test_two_distint_ships_same_day(self):
        """
        As this case contains a random return, it may fail rare cases. The test
        should test the sttistical distribution.
        """
        ships = [model.Ship(None, name="one", day=20, year=2070),
                 model.Ship(None, name="two", day=20, year=2070)]

        selected_ship_count = 0
        for i in range(100):
            new_ship = trader.get_earliest_ship(ships)
            if new_ship.name == "one":
                selected_ship_count += 1

        self.assertTrue(40 < selected_ship_count < 60)


        self.assertEqual(20, trader.get_earliest_ship(ships).day)