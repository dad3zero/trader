#!/usr/bin/env python 

import pytest
from startrader import trader as t
from startrader import model as m


@pytest.fixture()
def ship():
    return m.Ship(None, day=1, year=2070)


def test_add_one_day_to_ship(ship):
    t.update_ship_date(ship, 1)
    assert 2 == ship.day


def test_add_one_year_to_ship(ship):
    t.update_ship_date(ship, 360)
    assert 1 == ship.day
    assert 2071 == ship.year


def test_add_more_than_a_year(ship):
    t.update_ship_date(ship, 375)
    assert 16 == ship.day
    assert 2071 == ship.year


def test_add_more_than_two_year(ship):
    t.update_ship_date(ship, 735)
    assert 16 == ship.day
    assert 2072 == ship.year
